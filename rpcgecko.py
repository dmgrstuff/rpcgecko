# RPCGecko - written by dmgr_
# it's still spaghetti, but the sauce actually tastes good this time
# I've tried to put semi-serious comments on most things so feel free to look around

# we will now proceed to justify the bloat in my software
from colorama import Fore, Style, init # colorama makes ANSI escapes work on Windows/cmd
from pypresence import Presence, InvalidPipe # exception thrown when Discord is not open
from tcpgecko import TCPGecko # obvious
import csv # used for title database
import os # used for ui.cls()
import platform # used to get the platform name for the window title
import random # for unnecessary splash text
import re # regular expression
import requests # used for the updater
import struct # used for unpacking binary data from TCPGecko
import sys # used for sys.exit(0)
import time # used for time-related things
import webbrowser # also used in the updater
import yaml # used for parsing yaml (like config.yml and release.yml)

init() # colorama init
default_client = "798386017241399296" # the default Discord client ID

class config: # handles loading and saving configuration and titles.yml
    def __init__(self, cfg_file, titles):
        self.cfg_file = cfg_file
        self.titles = titles
        
    def load(self):
        try: f = open(self.cfg_file, "r")
        except (FileNotFoundError):
            ui.autoconfig()
            f = open(self.cfg_file, "r")
        cf = yaml.safe_load(f)
        f.close()
        return cf

    def dump(self, cf):
        with open(self.cfg_file, "w+") as f:
            yaml.dump(cf, f)
        with open(self.cfg_file, "a") as f:
            f.write("\n# Config generated by RPCGecko\n# Changing settings overwrites this file, so don't save any important data here!")
            f.close()
        return cf

    def load_titles(self):
        titles = {}
        read = csv.reader(open("titles.csv", "r", encoding="utf-8"))
        for row in read:
            key = row[0]
            titles[key] = row[1:]
        return titles

class interface: # handles UI functions

    def __init__(self, app_name, version): # UI class variables
        self.app_name = app_name
        self.version = version
        self.version_str = f"v{str(self.version)}"

    def about(self): # accessed by typing "about" in the menu
        ui.cls()
        print(f'''
    {b}{ui.app_name} {ui.version_str}{n} - Discord Rich Presence integration for the Wii U
    Written and rewritten by dmgr_ - https://github.com/dmgrstuff/rpcgecko
    
    Code for handling TCPGecko is based on a similar project:
    https://github.com/Rambo6Glaz/WiiU-DiscordRichPresence

    Thanks to Chadderz, Marionumber1, NWPlayer123, wj44, and all who contributed to TCPGecko's development.''')
        input("\n    ")
        ui.menu()

    def cls(self):
        os.system("cls" if os.name == "nt" else "clear") # should be cross-platform enough

    def header(self, text=None, error=None):
        if text is None: # if text is not passed to the function
            string = f"{self.app_name} {self.version_str}" # don't display it
        else:
            string = f"{self.app_name} {self.version_str} - {text}"
        output = f"{string}\n{'─' * len(string)}"
        if type(error) == str:
            output += error
        ui.cls() # since you're going to clear the terminal anyways
        return output # return the header whenever the function is called

    def truth(self, var): # this only exists to save me from unreadable one-liners
        if type(var) == str:
            if str.lower(var) == "y": return True
            elif str.lower(var) == "n": return False
        else:
            if var == True: return "yes"
            elif var == False: return "no"
        
    def autoconfig(self): # creates config.yml if it doesn't exist
        try: 
            print(ui.header("configuration"))
            print("Welcome to RPCGecko! Let's get set up.\n")
            ip = input("What is your Wii U's local IP address? ")
            var = input("Would you like to display your Nintendo Network ID on Discord? (y/N) ")
            if ui.truth(var) == True:
                show_nnid = True
                nnid = input("What is your Nintendo Network ID? ")
            else:
                show_nnid = False
                nnid = None
            cf = {"client_id": default_client, "custom_format": False, "ip": ip, "menu_splash": False, "nnid": nnid, "show_icons": True, "show_nnid": show_nnid, "status_format": "{title_name} ({title_code_short})", "update_csv": True} # default config
            cfg.dump(cf)
        except KeyboardInterrupt:
            print("\nClosing... (no configuration has been modified)")
            sys.exit(0)
        for sec in range(5, 0, -1):
            print(f"That's all we need for now. You can change these and other settings anytime in the menu or config.yml. ({sec})")
            time.sleep(1)
            print("\u001b[2A")

    def menu(self, error=None):
        if type(error) == str:
            print(ui.header() + error)
        else:
            print(ui.header())
        print("1. Connect to your Wii U (" + cf["ip"] + ") and start rich presence")
        print("2. Manually specify a title ID and start rich presence")
        print("3. Display title info from your console without takling to Discord")
        print(f"\n8. Check for updates")
        print("9. Settings")
        print("0. Exit\n")
        choice = input("Pick an option by typing its corresponding number. ")
        if choice == "1":
            rpc.init()
            ui.presence()
        elif choice == "2":
            rpc.init()
            ui.presence(refresh=False)
        elif choice == "3":
            ui.presence(rp=False)
        elif choice == "8":
            print(ui.header("updater"))
            ui.update_check()
        elif choice == "9":
            ui.settings()
        elif choice == "0":
            sys.exit(0)
        elif choice == "about":
            ui.about()
        elif choice != "":
            ui.menu(error=exc.invalid_input)
        ui.menu()
    
    def update_check(self, return_err=True):
        print("Checking for updates...")
        try: 
            response = requests.get("https://dmgrstuff.github.io/rpcgecko/release.yml")
            release = yaml.safe_load(response.text)
            if release["version"] > self.version: 
                choice = input("RPCGecko v" + str(release["version"]) + " is available. (you are using " + ui.version_str + ")\nWould you like to open the release page?\n[" + release["release_url"] + "] (y/N) ") # it's probably a good idea to tell the user what url they're about to open, right?
                if choice.lower() == "y":
                    webbrowser.open(release["release_url"]) # open the page in your default browser
                    sys.exit(0)
                else: pass
        except requests.exceptions.ConnectionError: ui.menu(exc.upd_conn_fail) # if connection fails
        except (yaml.scanner.ScannerError, KeyError, TypeError): ui.menu(exc.upd_keyerror) # else if some variable is missing or it can't be read for whatever reason
        if return_err == True: ui.menu(exc.upd_latest)
        else: ui.menu() # probably on startup, will loopback to menu

    def presence(self, rp=True, refresh=True):
        while True:
            if refresh == True:
                print(ui.header("connecting..."))
                try: title = tcp.title_info(tcp.read_title(cf["ip"]))
                except ConnectionResetError:
                    print(exc.conn_reset)
                    time.sleep(2)
                    ui.presence()
                print(ui.header("connected to " + cf["ip"]))
            else: 
                try: title = tcp.title_info(input("Please enter the 16-digit title ID of your game (format: 000500xx-xxxxxxxx): "))
                except KeyError: # probably ignore invalid input
                    pass
                if title["title_id"] == "": # except empty input
                    ui.menu()
                ui.cls()
                print(ui.header("title info"))
            print("Title name: " + title["title_name"])
            print("Title ID: " + title["title_id"])
            print("Title product code: " + title["title_code"])
            print("Title icon: " + title["title_icon"] + "\n")
            if rp == True:
                rpc.update(
                    title_id = title["title_id"],
                    title_name = title["title_name"],
                    title_code = title["title_code"],
                    title_code_short = title["title_code_short"],
                    title_icon = title["title_icon"],
                    nnid=cf["nnid"]
                ) # probably inefficient way to pass info to rich presence
            # sec = 15
            # while refresh == True: 
            if refresh == True:
                for sec in range(15, 0, -1):
                    print(f"Press Ctrl+C to stop. ({sec}) ")
                    time.sleep(1)
                    print("\u001b[2A")
                ui.presence(rp)
            input("Press enter to close rich presence. ")
            rpc.clear()
            ui.menu()
    
    def settings(self, error=None):
        text = "settings"
        if error is not None:
            print(ui.header(text, error=exc.invalid_input))
        else:
            print(ui.header(text))
        print("── RPCGecko ──")
        print("1. IP address: " + cf["ip"])
        print("2. Check for titles.csv updates: " + ui.truth(cf["update_csv"]))
        print("(disable this if you modified it yourself)")
        print("\n── Presence ──")
        print("3. Display large game icons: " + ui.truth(cf["show_icons"]))
        print("4. Display NNID: " + (ui.truth(cf["show_nnid"])))
        if cf["show_nnid"] == True:    
            if cf["nnid"] is None:
                print("5. Nintendo Network ID to display: not defined")
            else: print("5. Nintendo Network ID to display: " + cf["nnid"])
        print("6. Discord client ID: " + cf["client_id"])
        print("\n── Experimental (may cause weirdness!) ──")
        print("7. Enable custom presence text formatting: " + ui.truth(cf["custom_format"]))
        if cf["custom_format"] == True:
            print("8. Presence text format: " + cf["status_format"])

        if cf != cfg.load(): print(f"\n{yellow}0. Save changes and return to menu{n}") # check for changes, not optimal but it shouldn't be too slow
        else: print("\n0. Return to menu")
        choice = input("\nChoose an option to modify (y/n options will toggle): ")

        if choice == "1":
            i = input("Enter your Wii U's local IP address: ")
            if i != "": # don't overwrite variables with empty input
                cf["ip"] = i
        elif choice == "2":
            cf["update_csv"] = not cf["update_csv"]
        elif choice == "3":
            cf["show_icons"] = not cf["show_icons"]
        elif choice == "4":
            cf["show_nnid"] = not cf["show_nnid"]
        elif choice == "5" and cf["show_nnid"] == True:
            i = input("Enter your Nintendo Network ID: ")
            if i != "":
                cf["nnid"] = i
        elif choice == "6":
            i = input("Enter the client ID of your Discord application (or leave blank to revert to the default) ")
            if i != "": cf["client_id"] = i
            else: cf["client_id"] = default_client
        elif choice == "7":
            cf["custom_format"] = not cf["custom_format"]
        elif choice == "8":
            i = input("Enter the format for your Discord status. Variables should be surrounded by {}. (\n(variables: title_id, title_name, title_code, title_code_short, title_icon)\n")
            if i != "": cf["status_format"] = i
        elif choice == "0": # save config and exit
            cfg.dump(cf)
            ui.menu()
        elif choice != "": ui.settings(error=exc.invalid_input)
        ui.settings() # loop to keep the menu open

class exception_strings: # strings used for exception handling
    invalid_input = "\nThat's not a valid input.\n"
    conn_reset = "\nThe connection was reset - attempting to reconnect..."
    timeout = "\nThe connection timed out. Double check your console and network connection.\n"
    invalid_pipe = '\nMake sure the Discord client is running and try again. (InvalidPipe)\n'
    upd_conn_fail = "\nChecking for updates failed. Please double check your connection.\n"
    upd_keyerror = "\nChecking for updates failed because release.yml could not be parsed.\n"
    upd_latest = "\nNo updates are available.\n"

class tcp: # handles everything TCPGecko related
    def connect(self, ip):
        try: self.tcp = TCPGecko(ip) # connect to the console
        except ConnectionResetError: # this probably won't occur, but might as well be safe
            ui.cls()
            ui.header("reconnecting...")
            print(exc.conn_reset)
            time.sleep(2) # really just gives you enough time to see the message, this is rather pointless
        except TimeoutError:
            ui.cls()
            ui.menu(error=exc.timeout)
    def read_title(self, ip):
        tcp.connect(ip)
        read = re.findall("........" , "000" + str(format(struct.unpack(">Q", self.tcp.readmem(0x10013C10, 8))[0] , "x")))
        return (read[0] + "-" + read[1]).upper() # making title ids case insensitive, more or less
    def title_info(self, title_id):
        try:
            title_name = titles()[title_id][0]
            title_code = titles()[title_id][1]
            title_icon = titles()[title_id][2]
            try: title_code_short = title_code[6:10] # truncating the product code to four letters (ex. AGME)
            except IndexError: # which can fail on some titles that don't have a product code in titles.csv
                title_code_short = "-" # so we handle it
            if title_icon == "":
                title_icon = "wiiu" # default icon, there's probably a better way to do this
        except KeyError: # usually manual entry that isn't in titles.csv
            return {
                "title_id": title_id,
                "title_name": "", 
                "title_code": "",
                "title_icon": "wiiu",
                "title_code_short": ""
                }        
        return { # normal return
            "title_id": title_id, # this isn't necessary
            "title_name": title_name,
            "title_code": title_code,
            "title_icon": title_icon,
            "title_code_short": title_code_short
        }

class rpc: # handles everything rich presence related
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = Presence(client_id)
    def init(self): # initializes the RPC connection
        global start_time # someone will probably yell at me for using a global variable here
        try: 
            self.rpc.connect()
            start_time = str(int(time.time())) # and yes there's probably a more pythonic way but whatever
        except InvalidPipe:
            ui.menu(exc.invalid_pipe)
    def update(self, title_id, title_name, title_code, title_code_short, title_icon, nnid=None):
        if cf["custom_format"] == True:
            details = cf["status_format"].format(title_id=title_id, title_name=title_name, title_code=title_code, title_code_short=title_code_short, title_icon=title_icon)
        else:
            if title_code == "": details = title_name # graceful handling of empty variables  
            elif title_name == "": details = "Playing a game"
            else: details = f"{title_name} ({title_code_short})" # the default status format
        if cf["show_icons"] == False: title_icon = None # simple way to prevent icons from displaying, I think
        if cf["show_nnid"] == False: small_image = None # this will also not be displayed if you don't specify a large image
        else: small_image = "nnid"
        self.rpc.update( # all the info that gets sent to Discord
            details=details,
            large_image=title_icon,
            small_image=small_image,
            large_text=f'{ui.app_name} 🦎 {ui.version_str}',
            small_text=nnid,
            start=start_time,
        )
    def clear(self):
        self.rpc.clear() # clears 

# shorthand text formatting
b = Style.BRIGHT
n = Style.RESET_ALL
yellow = Fore.YELLOW

# Initialize classes
ui = interface('RPCGecko', 1.0) # sets the app name and version number (for header and updater)
exc = exception_strings()
tcp = tcp()

# Load settings and title database
cfg = config("config.yml", "titles.yml")
cf = cfg.load()
titles = cfg.load_titles

# Init RPC class with client id from config.yml
try: rpc = rpc(cf["client_id"]) 
except (TypeError, KeyError): ui.autoconfig()
print(f"\033]0;{ui.app_name} {ui.version_str} ({platform.system()})\007", end="") # window title
try: 
    ui.cls()
    ui.update_check(return_err=False) # checks for updates on startup, you could effectively disable this by replacing it with ui.menu()
except KeyboardInterrupt: # handle Ctrl+C a little more gracefully
    print("Closing...")
    sys.exit(0)
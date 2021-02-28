![RPCGecko - a configurable Discord Rich Presence app for the Wii U](https://dmgrstuff.github.io/rpcgecko/img/header.png)

## Usage

Download the [latest release](https://github.com/dmgrstuff/rpcgecko/releases/latest) and run the executable, or see the [build instructions](https://github.com/dmgrstuff/rpcgecko/blob/main/docs/building.md) to build or run it from source.

RPCGecko will ask for your Wii U's local IP address as well as your Nintendo Network ID if you choose to display it. A `config.yml` file will be created in the same directory so you'll want to put the executable somewhere convenient. You can change any of these settings from within the application or by editing the file manually.

Once you run the TCPGecko Installer on your Wii U, you can connect to it in RPCGecko's terminal-based menu.

## Known issues

#### RPCGecko bugs/limitations

- Icons don't display for every title because Discord requires assets to be pre-uploaded - see [custom-assets.md](https://github.com/dmgrstuff/rpcgecko/blob/main/docs/custom-assets.md) for more info and a simple workaround.
- Reading from memory (and refreshing Rich Presence) can hang sometimes, and closing your terminal in this case will probably freeze your console.

#### TCPGecko limitations

- Some applications (**YouTube**, for example) might freeze your console if TCPGecko is running. Also, system applets like the **Friends List** and **Internet Browser** can cause TCPGecko to hang until you exit them.
- Exiting **System Settings** will unload TCPGecko and other memory resident homebrew. You'll need to re-run the TCPGecko Installer to continue using RPCGecko.
- vWii will likely never be supported because of the way backwards compatibility works on the Wii U.

RPCGecko is a **work-in-progress**, so feel free to make an issue or pull request if you run into problems.

## Credits

**Rambo6Glaz** and **twosecslater** for the idea behind this project and [some implementations](https://github.com/NexoDevelopment/WiiU-DiscordRichPresence) that helped me

**Chadderz**, **Marionumber1**, **NWPlayer123**, **wj44**, and all who contributed to the development of TCPGecko

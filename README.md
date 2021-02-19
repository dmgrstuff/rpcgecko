![RPCGecko - a configurable Discord Rich Presence app for the Wii U](https://dmgrstuff.github.io/rpcgecko/img/header.png)

## Usage

Download the [latest release](https://github.com/dmgrstuff/rpcgecko/releases/latest) and run the executable, or see the [build instructions](https://github.com/dmgrstuff/rpcgecko/blob/main/docs/building.md) to build or run it from source.

The first time you run RPCGecko, it will ask for your Wii U's local IP address as well as your Nintendo Network ID if you want to display it. A `config.yml` file will be created in the same directory so you'll want to put the executable somewhere convenient. You can change any of these settings from within the application or by editing the file manually.

Once TCPGecko is running on your Wii U, you can connect to it (and Discord) in RPCGecko's terminal-based menu.

## Known issues

#### RPCGecko limitations

- Not all Wii U games will display icons in your status - this is because Discord requires Rich Presence assets to be manually uploaded to their developer portal. If a game you play doesn't have an icon (which is likely the case), it is possible to [add your own](https://github.com/dmgrstuff/rpcgecko/blob/main/docs/custom-assets.md).

#### TCPGecko limitations

- TCPGecko can cause some applications, like **YouTube**, to freeze your console. Also, apps accessible through the in-game HOME Menu (like the **Friends List** and **Internet Browser**) can cause TCPGecko to hang until you exit them.
- Exiting **System Settings** will unload TCPGecko (and other homebrew) from memory. This will cause the connection to timeout and you'll need to re-run the TCPGecko Installer to continue using RPCGecko.
- vWii will likely never be supported because of the way backwards compatibility works on the Wii U.

If you find something else that doesn't work or just need help, feel free to file an issue and I'll try to help you out as best I can.

## Credits

**Rambo6Glaz** and **twosecslater** for the idea behind this project and [some implementations](https://github.com/NexoDevelopment/WiiU-DiscordRichPresence) that helped me

**Chadderz**, **Marionumber1**, **NWPlayer123**, **wj44**, and all who contributed to the development of TCPGecko

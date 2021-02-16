# Adding your own assets to RPCGecko

A lot of Wii U games don't have icons in RPCGecko, and **this is not a bug!** Because of the way Rich Presence works, I have to pre-upload all the assets I want to use (with a max of 150 images) to Discord's developer portal, so some games will only show the default "Wii U" logo.

While I'm working on adding support for more titles, it's actually really simple to add your own by making your own Discord application with your desired assets, and there are only a couple steps to make it stick in RPCGecko. Here's how you can do it.

**1.** Go to the [Discord Developer Portal](https://discord.com/developers) and log in with your Discord account if you're prompted to. Create a new application and give it a name. This name shows under your "Playing" status, so you might want to call it `Wii U` or something similar.

**2.** Under `Rich Presence`, upload your assets and give them a name without spaces. Discord requires these images to be at least 512x512, but upscaling smaller images with something like [waifu2x](https://waifu2x.udp.jp) or just resizing them in an image editor usually gives decent results since Discord doesn't display them very large anyways.

(The icons I've included under `/assets` are just 128x icons, dumped from the title contents and run through waifu2x twice, if you're wondering.)

**3.** Go back to `General Information` and copy the client ID - you'll need it later to point RPCGecko to the application with your custom assets.

**4.** Open `titles.csv` in Excel, LibreOffice Calc, or just a basic text editor. Search for your game's name and insert the name you chose in the developer portal for its icon under the `title_icon` column (or after the fourth `,`). Save the file and close your editor.

**5.** Open RPCGecko, choose `Settings`, then `Discord client ID`. Paste the client ID you copied from the developer portal here.

Assuming you did everything here (and gave Discord a bit of time to cache the assets), you should now see custom icons in your Discord status when RPCGecko is connected.

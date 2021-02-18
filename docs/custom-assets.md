# Adding your own assets to RPCGecko

Because of the way Rich Presence works, a lot of Wii U games don't have icons in RPCGecko. All assets have to be pre-uploaded to Discord before you can use them.

However, it's very simple to work around this by making a Discord application with your desired assets, and there are only a couple steps to make it stick in RPCGecko. Here's how:

**1.** First off, collect your assets. You can always make your own, but a couple methods of getting icons that I've used include:
- Dumping them from your console with FTPiiU Everywhere
- Getting them from a database like [steamgriddb.com/projects/wii-u](https://www.steamgriddb.com/projects/wii-u)

You'll need to resize these to at least 512x512 for Discord to accept them. [waifu2x](https://waifu2x.udp.jp) works pretty well for this, but any image editor or upscaler will do.

**2.** Go to the [Discord Developer Portal](https://discord.com/developers) and log in with your Discord account if you're prompted to. Create a new application and give it a name.

**This name is displayed under your "Playing" status, so you might want to call it `Wii U` or something similar.**

**3.** Under `Rich Presence`, upload your assets and give all of them a name.

**4.** Go back to `General Information` and copy the client ID - you'll need it later to point RPCGecko to the application with your custom assets.

**5.** Open `icons.yml` and add a line for each asset you uploaded earlier using this format:

```yml
title_id: asset_name

# example: Mario Kart 8, US
00050000-1010EC00: mario_kart_8
```

You can find the 16-digit title ID of your game in WiiUBrew's [title database](https://wiiubrew.org/wiki/Title_database). The assets referenced by default are available in the `/assets` folder.

**6.** Change the client ID in RPCGecko's settings or `config.yml` to the one you copied earlier.

Once Discord caches your assets (which shouldn't take long), you should now see your custom icons in your status when RPCGecko is connected.

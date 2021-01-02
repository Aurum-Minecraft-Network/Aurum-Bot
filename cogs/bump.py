import json
import discord
from discord.ext import commands
import asyncio

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global bumpDone
        bumpDone = False

    @commands.command()
    async def bumpreset(self, ctx, boolw):
        if str(ctx.author.id) == "438298127225847810":
            global bumpDone
            if boolw == "True":
                bumpDone = "True"
            else:
                bumpDone = "False"
            await ctx.send(f"Done. `bumpDone` has been set to `{boolw}`!")
        else:
            await ctx.send("Sorry, but you do not have permission to do that.")

    @commands.Cog.listener()
    async def on_message(self, message):
        global bumpDone
        if str(message.channel.id) == "793523006172430388" and str(message.author.id) == "302050872383242240" and not bumpDone and message.embeds[0].description.endswith("""      Bump done :thumbsup:
      Check it on DISBOARD: https://disboard.org/"""):
            bumpDone = True
            cmd = await message.channel.history(limit=1, before=message.id).flatten()[0]
            if cmd.content == "!d bump":
                with open("bumping.json", "r") as f:
                    bumps = json.load(f)
                if str(cmd.author.id) in bumps:
                    bumpno = int(bumps[str(cmd.author.id)])
                    bumps[str(cmd.author.id)] = bumpno + 1
                else:
                    bumps.update({f"{str(cmd.author.id)}": "1"})
                with open("bumping.json", "w") as f:
                    json.dump(bumps, f, indent=4)
            await message.channel.send(f"Bump succeeded. Thanks, <@{cmd.author.id}>.\nNext bump in 2 hours")
            await message.delete(delay=3)
            await asyncio.sleep(7200) # Wait for 2 hours
            await message.channel.send("<@793661769125986384>, it is time to bump! Use `!d bump` now.")
            bumpDone = False
        elif bumpDone and str(message.author.id) == "302050872383242240" and message.embeds[0].description.endswith("until the server can be bumped"):
            minutes = [int(i) for i in message.embeds[0].description.split() if i.isdigit()]
            await message.delete()
            await message.channel.send(f"Sorry, but you need to wait **{str(minutes[0])}** minutes in order to bump again.")
        await self.bot.process_commands(message)
    
def setup(bot):
    bot.add_cog(Bump(bot))

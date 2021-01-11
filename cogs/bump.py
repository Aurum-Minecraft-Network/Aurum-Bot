import json
import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio
import traceback
from datetime import datetime, timedelta

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bumpkingupdate.start()

    async def getBumps(self):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798226999238983750)
        return json.loads(msg.content)

    async def updateBumps(self, dict):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798226999238983750)
        await msg.edit(content=json.dumps(dict, indent=4))

    @commands.Cog.listener()
    async def on_ready(self):
        global bumpDone
        global reminded
        global bumpCount
        bumpDone = False
        reminded = False
        bumpCount = datetime.now()

    @commands.command()
    async def bumpreset(self, ctx, boolw):
        if str(ctx.author.id) == "438298127225847810":
            global bumpDone
            if boolw == "True":
                bumpDone = True
            elif boolw == "False":
                bumpDone = False
            else:
                await ctx.send("Invalid param!")
            await ctx.send(f"Done. `bumpDone` has been set to `{boolw}`!")
        else:
            await ctx.send("Sorry, but you do not have permission to do that.")

    @commands.command(aliases=["bumpleader"])
    async def bumpleaderboard(self, ctx):
        bumps = await self.getBumps()
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
        leaderv = list(leaders.values())
        leaderk = list(leaders.keys())
        msg = "**__Bump Leaderboard__**"
        rank = int(leaderv[0])
        place = 1
        usersDone = 0
        for name, bumpe in zip(leaderk, leaderv):
            guild = self.bot.get_guild(793495102566957096)
            for users in guild.members:
                if str(users.id) == str(name):
                    user = users
                else:
                    continue
                if rank > int(bumpe):
                    place += 1
                    rank = int(leaderv[usersDone])
                msg += f"\n{str(place)}. {user.name}#{user.discriminator} - {rank} Bump"
                if int(bumpe) > 1:
                    msg += "s"
                usersDone += 1
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        global bumpDone
        if str(message.channel.id) == "793523006172430388" and str(message.author.id) == "302050872383242240" and not bumpDone and message.embeds[0].description.endswith("""      Bump done :thumbsup:
      Check it on DISBOARD: https://disboard.org/"""):
            bumpDone = True
            cmd = (await message.channel.history(limit=1, before=message).flatten())[0]
            if cmd.content == "!d bump":
                bumps = await self.getBumps()
                if str(cmd.author.id) in bumps:
                    bumpno = int(bumps[str(cmd.author.id)])
                    bumps[str(cmd.author.id)] = int(bumpno + 1)
                else:
                    bumps.update({f"{str(cmd.author.id)}": 1})
                await self.updateBumps(bumps)
            await message.channel.send(f"Bump succeeded. Thanks, <@{cmd.author.id}>!\nNext bump in 2 hours")
            global channelyeet
            channelyeet = message.channel
            await message.delete()
            global bumpCount
            bumpCount = datetime.now()
        elif bumpDone and str(message.author.id) == "302050872383242240" and message.embeds[0].description.endswith("until the server can be bumped"):
            minutes = [int(i) for i in message.embeds[0].description.split() if i.isdigit()] # Function to extract numbers from a string
            await message.delete()
            await message.channel.send(f"Sorry, but you need to wait **{str(minutes[0])}** minutes in order to bump again.")
        elif str(message.channel.id) == "793523006172430388" and ((message.content != "!d bump" or message.content != "a!bumpleader" or message.content != "a!bumpleaderboard") and str(message.author.id) != "793546056934883328"):
            await message.delete()
    
    @tasks.loop(seconds=10)
    async def bumpreminder(self):
        if 'reminded' not in vars():
            global reminded
            reminded = False
        elif not reminded:
            global bumpCount
            try:
                if datetime.now() - timedelta(hours=2) > bumpCount:
                    await channelyeet.send("<@&793661769125986384>, it is time to bump! Use `!d bump` now.")
                    global bumpDone
                    bumpDone = False
                    reminded = True
            except NameError:
                bumpCount = datetime.now()

    @bumpreminder.before_loop
    async def before_bumpreminder(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=30)
    async def bumpkingupdate(self):
        try:
            bumps = await self.getBumps()
            bumpsRank = dict(sorted(bumps.items(), key=lambda item: item[1])) # Function to rank dictionary
            bumpKingValue = int(list(bumpsRank.values())[-1])
            guild = self.bot.get_guild(793495102566957096)
            bumpKing = get(guild.roles, id=795477556122877995)
            bumpKings = []
            newBumpKings = []
            addBumpKings = []
            removeBumpKings = []
            for user in guild.members:
                if bumpKing in user.roles:
                    bumpKings.append(user)
            if len(bumpKings) != 1:
                if len(bumpKings) < 0:
                    print("What the fuck")
                elif len(bumpKings) == 0:
                    pass
                elif len(bumpKings) > 1:
                    pass
            for user in guild.members:
                try:
                    if int(bumps[str(user.id)]) == bumpKingValue:
                        newBumpKings.append(user)
                except KeyError:
                    continue
            if not bumpKings == newBumpKings:
                for user in newBumpKings:
                    if user not in bumpKings:
                        addBumpKings.append(user)
                for user in bumpKings:
                    if user not in newBumpKings:
                        removeBumpKings.append(user)
            noice = "All hail the new Bump King"
            if len(addBumpKings) > 1:
                noice += "s"
            for user in addBumpKings:
                noice += f" <@{user.id}>"
            noice += "!"
            bumpChannel = self.bot.get_channel(793523006172430388)
            if len(addBumpKings) > 0:
                await bumpChannel.send(noice)
            for user in addBumpKings:
                await user.add_roles(bumpKing)
            for user in removeBumpKings:
                await user.remove_roles(bumpKing)
        except:
            traceback.print_exc()

    @bumpkingupdate.before_loop
    async def before_bumpkingupdate(self):
        await self.bot.wait_until_ready()
    
def setup(bot):
    bot.add_cog(Bump(bot))

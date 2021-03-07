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
        self.bumpreminder.start()

    async def getBumps(self): # Get bump JSON string from channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798226999238983750)
        return json.loads(msg.content)

    async def updateBumps(self, dict): # Edit the JSON string in the channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798226999238983750)
        await msg.edit(content=json.dumps(dict, indent=4))

    async def getTime(self): # Get the time representation string from channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(799962496118292491)
        return datetime.strptime(msg.content, "%Y-%m-%d %H:%M:%S.%f")

    async def updateTime(self, time): # Update the time representation string in the channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(799962496118292491)
        await msg.edit(content=datetime.strftime(time, "%Y-%m-%d %H:%M:%S.%f"))

    @commands.Cog.listener()
    async def on_ready(self):
        global bumpDone
        global reminded
        bumpDone = False
        reminded = False

    @commands.command()
    async def bumpreset(self, ctx, boolw): # Set whether the bot thinks the server has been bumped in the last 2 hours
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
        bumps = await self.getBumps() # Get bump data of all users
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True)) # Sort the dictionary from user with most bumps to least bumps
        leaderv = list(leaders.values()) # Number of bumps
        leaderk = list(leaders.keys()) # User ID
        msg = "**__Bump Leaderboard__**"
        rank = int(leaderv[0]) # Highest number of bumps
        place = 1
        usersDone = 0
        for name, bumpe in zip(leaderk, leaderv):
            guild = self.bot.get_guild(793495102566957096)
            for users in guild.members:
                if str(users.id) == str(name):
                    user = users # Found the user in the guild which the user ID represents
                else:
                    continue
                if rank > int(bumpe): # This user has less bumps than the previous user
                    place += 1 # So he/ she is one place lower
                    rank = int(leaderv[usersDone]) # Set rank to the number of bumps done by this user
                ## else: pass
                ## Same no. of bumps as the previous user, same place!
                msg += f"\n{str(place)}. {user.name}#{user.discriminator} - {rank} Bump"
                ## Should we make the word "Bump" plural?
                if int(bumpe) > 1:
                    msg += "s"
                usersDone += 1
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        global bumpDone
        ## Bump succeeded
        if str(message.channel.id) == "793523006172430388" and str(message.author.id) == "302050872383242240" and not bumpDone and message.embeds[0].description.endswith("""      Bump done :thumbsup:
      Check it on DISBOARD: https://disboard.org/"""):
            bumpDone = True
            cmd = (await message.channel.history(limit=1, before=message).flatten())[0] # Get the message before this message
            if cmd.content == "!d bump":
                self.bumpreminder.cancel()
                bumps = await self.getBumps()
                ## Update the bumps JSON string
                if str(cmd.author.id) in bumps:
                    bumpno = int(bumps[str(cmd.author.id)])
                    bumps[str(cmd.author.id)] = int(bumpno + 1)
                else:
                    bumps.update({f"{str(cmd.author.id)}": 1})
                try:
                    if bumps["lastBump"][0] == str(cmd.author.id):
                        bumps.update({"lastBump": [str(cmd.author.id), bumps["lastBump"][1] + 1]})
                    else:
                        bumps.update({"lastBump": [str(cmd.author.id), 1]})
                except KeyError:
                    bumps["lastBump"] = [str(cmd.author.id), 1]
                await self.updateBumps(bumps)
            bumpDone = True
            global reminded
            reminded = False
            msg = "Bump succeeded. Thanks, <@{cmd.author.id}>!"
            if bumps["lastBump"][1] > 1:
                msg += f"""\n**{bumps["lastBump"][1]} COMBO :fire:**"""
            msg += "\nNext bump in 2 hours"
            await message.channel.send(f"Bump succeeded. Thanks, <@{cmd.author.id}>!\nNext bump in 2 hours")
            global channelyeet
            channelyeet = message.channel
            await message.delete()
            await self.updateTime(datetime.now()) # Set time bumped
            self.bumpreminder.start()
        ## Need to wait until bump
        elif bumpDone and str(message.author.id) == "302050872383242240" and message.embeds[0].description.endswith("until the server can be bumped"):
            minutes = [int(i) for i in message.embeds[0].description.split() if i.isdigit()] # Function to extract numbers from a string
            await message.delete()
            await message.channel.send(f"Sorry, but you need to wait **{str(minutes[0])}** minutes in order to bump again.")
        ## Disallowed messages
        elif str(message.channel.id) == "793523006172430388" and message.content not in ['!d bump', 'a!bumpleader', 'a!bumpleaderboard'] and str(message.author.id) not in ["793546056934883328", "438298127225847810"]:
            await message.delete()
    
    @tasks.loop(seconds=10) # Function to see whether we have to remind users to bump
    async def bumpreminder(self):
        if 'reminded' not in vars():
            global reminded
            reminded = False
        if 'channelyeet' not in vars():
            global channelyeet
            channelyeet = self.bot.get_channel(793523006172430388)
        global bumpDone
        if not reminded and bumpDone:
            if datetime.now() - timedelta(hours=2) > (await self.getTime()): # Has it been 2 hours?
                await channelyeet.send("<@&793661769125986384>, it is time to bump! Use `!d bump` now.")
                bumpDone = False
                reminded = True

    @bumpreminder.before_loop
    async def before_bumpreminder(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=30)
    async def bumpkingupdate(self):
        try:
            bumps = await self.getBumps()
            del bumps["lastBump"]
            bumpsRank = dict(sorted(bumps.items(), key=lambda item: item[1])) # Function to rank dictionary from user with lowest bumps to highest
            bumpKingValue = int(list(bumpsRank.values())[-1]) # Highest value of bumps!
            guild = self.bot.get_guild(793495102566957096)
            bumpKing = get(guild.roles, id=795477556122877995)
            bumpKings = []
            newBumpKings = []
            addBumpKings = []
            removeBumpKings = []
            for user in guild.members:
                if bumpKing in user.roles:
                    bumpKings.append(user) # Get list of bump kings
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
                        newBumpKings.append(user) # He is a bump king
                except KeyError:
                    continue
            if not bumpKings == newBumpKings: # Change needed!
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

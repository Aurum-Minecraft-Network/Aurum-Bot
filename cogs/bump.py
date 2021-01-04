import json
import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio
import traceback

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bumpkingupdate.start()

    @commands.Cog.listener()
    async def on_ready(self):
        global bumpDone
        bumpDone = False

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
        with open("bumps.json", "r") as f:
            bumps = json.load(f)
        print(bumps)
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
        print(leaders)
        leaderv = list(leaders.values())
        leaderk = list(leaders.keys())
        print(leaderv, leaderk)
        msg = "**__Bump Leaderboard__**"
        rank = int(leaderv[0])
        place = 1
        usersDone = 0
        for name, bumpe in zip(leaderk, leaderv):
            print(name)
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
                with open("bumps.json", "r") as f:
                    bumps = json.load(f)
                if str(cmd.author.id) in bumps:
                    bumpno = int(bumps[str(cmd.author.id)])
                    bumps[str(cmd.author.id)] = int(bumpno + 1)
                else:
                    bumps.update({f"{str(cmd.author.id)}": 1})
                with open("bumps.json", "w") as f:
                    json.dump(bumps, f, indent=4)
            await message.channel.send(f"Bump succeeded. Thanks, <@{cmd.author.id}>!\nNext bump in 2 hours")
            channelyeet = message.channel
            await message.delete()
            print("Bump countdown has started.")
            await asyncio.sleep(7200) # Wait for 2 hours
            await channelyeet.send("<@&793661769125986384>, it is time to bump! Use `!d bump` now.")
            bumpDone = False
        elif bumpDone and str(message.author.id) == "302050872383242240" and message.embeds[0].description.endswith("until the server can be bumped"):
            minutes = [int(i) for i in message.embeds[0].description.split() if i.isdigit()] # Function to extract numbers from a string
            await message.delete()
            await message.channel.send(f"Sorry, but you need to wait **{str(minutes[0])}** minutes in order to bump again.")
    
    @tasks.loop(seconds=30)
    async def bumpkingupdate(self):
        try:
            print("Checking for new bump kings now!")
            with open("bumps.json", "r") as f:
                bumps = json.load(f)
            bumpsRank = dict(sorted(bumps.items(), key=lambda item: item[1])) # Function to rank dictionary
            bumpKingValue = int(list(bumpsRank.values())[-1])
            print(bumpKingValue, bumpsRank)
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
                    for user in bumpKings:
                        await user.remove_roles(bumpKing)
            for user in guild.members:
                try:
                    if int(bumps[str(user.id)]) == bumpKingValue:
                        newBumpKings.append(user)
                except KeyError:
                    continue
            if bumpKings == newBumpKings:
                if len(bumpKings) > 1:
                    for user in bumpKings:
                        await user.add_roles(bumpKing)
            else:
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

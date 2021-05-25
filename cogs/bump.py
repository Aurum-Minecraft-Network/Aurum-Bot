import json
import discord
from discord.ext import tasks, commands
from discord.utils import get
import traceback
from datetime import datetime, timedelta
from discord_slash import cog_ext, SlashContext
from typing import Union

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bumpkingupdate.start()
        self.bumpreminder.start()
        self.denyDisboardAccess.start()
            
    def convert(seconds): # Take x seconds and returns a hours, b minutes, c seconds
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return (hour, min, sec)
    
    async def sendNoPermission(self, ctx: Union[discord.ext.commands.Context, SlashContext, discord.TextChannel, discord.DMChannel, discord.GroupChannel]):
        emojis = self.bot.get_guild(846318304289488906).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} Error: No Permission", description="Sorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

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
        guild = self.bot.get_guild(793495102566957096)
        bumpChannel = guild.get_channel(793523006172430388)
        disboard = guild.get_member(302050872383242240)
        if disboard.status == discord.Status.offline:
            await bumpChannel.set_permissions(guild.default_role, send_messages=False)
            self.bumpreminder.cancel()
            bumpDone = True
            print("DISBOARD now off")
        elif disboard.status == discord.Status.online:
            await bumpChannel.set_permissions(guild.default_role, send_messages=True)
            try:
                self.bumpreminder.start()
            except RuntimeError:
                pass
            finally:
                bumpDone = False
            print("DISBOARD now on")
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.id == 302050872383242240 and after.id == 302050872383242240:
            guild = self.bot.get_guild(793495102566957096)
            bumpChannel = guild.get_channel(793523006172430388)
            if before.status == after.status:
                pass
            elif before.status == discord.Status.online and after.status == discord.Status.offline:
                emojis = self.bot.get_guild(846318304289488906).emojis
                embed = discord.Embed(title=f"{get(emojis, name='error')} DISBOARD Status", description="<@302050872383242240> is currently offline!", color=0x36393f)
                await bumpChannel.send(embed=embed)
                self.bumpreminder.cancel()
                print("DISBOARD now off")
            elif before.status == discord.Status.offline and after.status == discord.Status.online:
                emojis = self.bot.get_guild(846318304289488906).emojis
                embed = discord.Embed(title=f"{get(emojis, name='error')} DISBOARD Status", description="<@302050872383242240> is currently online!", color=0x36393f)
                await bumpChannel.send(embed=embed)
                self.bumpreminder.start()
                print("DISBOARD now on")
                
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
            await self.sendNoPermission(ctx=ctx)

    @commands.command(aliases=["bumpleader"])
    async def bumpleaderboard(self, ctx):
        bumpss = await self.getBumps() # Get bump data of all users
        bumps = bumpss
        del bumps["lastBump"]
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True)) # Sort the dictionary from user with most bumps to least bumps
        leaderv = list(leaders.values()) # Number of bumps
        leaderk = list(leaders.keys()) # User ID
        msg = ""
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
                if rank > 1:
                    msg += "s"
                usersDone += 1
        emojis = self.bot.get_guild(846318304289488906).emojis
        embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Bump Leaderboard", description=msg, color=0x36393f)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        global bumpDone
        ## Bump succeeded
        if str(message.channel.id) == "793523006172430388" and str(message.author.id) == "302050872383242240" and not bumpDone and message.embeds[0].description.endswith("""      Bump done :thumbsup:
      Check it on DISBOARD: https://disboard.org/"""):
            bumpDone = True
            ## Get the person who bumped
            bumpUser = self.bot.get_guild(793495102566957096).get_member(int(message.embeds[0].description.split(",")[0].replace("<", "").replace(">", "").replace("@", "")))
            self.bumpreminder.cancel()
            bumps = await self.getBumps()
            ## Update the bumps JSON string
            if str(bumpUser.id) in bumps:
                bumpno = int(bumps[str(bumpUser.id)])
                bumps[str(bumpUser.id)] = int(bumpno + 1)
            else:
                bumps.update({f"{str(bumpUser.id)}": 1})
            try:
                if str(bumps["lastBump"][0]) == str(bumpUser.id):
                    bumps.update({"lastBump": [str(bumpUser.id), (int(bumps["lastBump"][1]) + 1)]})
                else:
                    bumps.update({"lastBump": [str(bumpUser.id), 1]})
            except KeyError:
                bumps["lastBump"] = [str(bumpUser.id), 1]
            await self.updateBumps(bumps)
            bumpDone = True
            global reminded
            reminded = False
            guild = self.bot.get_guild(793495102566957096)
            await message.channel.set_permissions(guild.default_role, send_messages=False)
            print("Bumped, locked")
            msg = ""
            if int(bumps["lastBump"][1]) > 1:
                msg += f"""**{bumps["lastBump"][1]} COMBO :fire:**\n"""
            emojis = self.bot.get_guild(846318304289488906).emojis
            embed = discord.Embed(title=f"Thanks {bumpUser.name}!", description=msg + "Bump succeeded. Next bump is in 2 hours.", color=0x36393f)
            await message.channel.send(embed=embed)
            global channelyeet
            channelyeet = message.channel
            await message.delete()
            await self.updateTime(datetime.now()) # Set time bumped
            self.bumpreminder.start()
        ## Need to wait until bump
        elif bumpDone and str(message.author.id) == "302050872383242240" and message.embeds[0].description.endswith("until the server can be bumped"):
            minutes = [int(i) for i in message.embeds[0].description.split() if i.isdigit()] # Function to extract numbers from a string
            await message.delete()
            emojis = self.bot.get_guild(846318304289488906).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Bump Cooldown", description=f"Sorry, but you need to wait **{str(minutes[0])}** minutes in order to bump again.", color=0x36393f)
            await message.channel.send(embed=embed)
        ## Disallowed messages
        elif str(message.channel.id) == "793523006172430388" and message.content not in ['!d bump', 'a!bumpleader', 'a!bumpleaderboard'] and str(message.author.id) not in ["793546056934883328", "438298127225847810", "302050872383242240"]:
            await message.delete()
        
    @tasks.loop(seconds=10)
    async def denyDisboardAccess(self):
        guild = self.bot.get_guild(793495102566957096)
        role = discord.utils.get(guild.roles, id=821408975811379210)
        for channel in guild.channels:
            if channel.name != "bumping":
                await channel.set_permissions(role, read_messages=False)
                
    @denyDisboardAccess.before_loop
    async def before_denyDisboardAccess(self):
        await self.bot.wait_until_ready()
    
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
            if datetime.now() - timedelta(hours=2, seconds=30) > (await self.getTime()): # Has it been 2 hours?
                guild = self.bot.get_guild(793495102566957096)
                emojis = self.bot.get_guild(846318304289488906).emojis
                embed = discord.Embed(title=f"{get(emojis, name='bump')} Bump Reminder", description="Bumpers, it is time to bump! Use `!d bump` now.", color=0x36393f)
                await channelyeet.send(embed=embed)
                await channelyeet.send("<@&793661769125986384>")
                await channelyeet.set_permissions(guild.default_role, send_messages=True)
                print("Can bump now, unlocked")
                bumpDone = False
                reminded = True

    @bumpreminder.before_loop
    async def before_bumpreminder(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=30)
    async def bumpkingupdate(self):
        try:
            bumps = await self.getBumps() # Get bump data of all users
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
            title = "All hail the new Bump King"
            noice = ""
            if len(addBumpKings) > 1:
                title += "s"
            for user in addBumpKings:
                noice += f" <@{user.id}>"
            bumpChannel = self.bot.get_channel(793523006172430388)
            if len(addBumpKings) > 0:
                emojis = self.bot.get_guild(846318304289488906).emojis
                embed = discord.Embed(title=str(get(emojis, name='bump')) + title, description=noice + "!", color=0x36393f)
                await bumpChannel.send(embed=embed)
            for user in addBumpKings:
                await user.add_roles(bumpKing)
            for user in removeBumpKings:
                await user.remove_roles(bumpKing)
        except:
            traceback.print_exc()

    @bumpkingupdate.before_loop
    async def before_bumpkingupdate(self):
        await self.bot.wait_until_ready()
        
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="bumpleader",
                       description="Gives a leaderboard of bumps",
                       guild_ids=[guildID])
    async def _bumpleader(self, ctx: SlashContext):
        bumpss = await self.getBumps() # Get bump data of all users
        bumps = bumpss
        del bumps["lastBump"]
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True)) # Sort the dictionary from user with most bumps to least bumps
        leaderv = list(leaders.values()) # Number of bumps
        leaderk = list(leaders.keys()) # User ID
        msg = ""
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
                if rank > 1:
                    msg += "s"
                usersDone += 1
        emojis = self.bot.get_guild(846318304289488906).emojis
        embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Bump Leaderboard", description=msg, color=0x36393f)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Bump(bot))

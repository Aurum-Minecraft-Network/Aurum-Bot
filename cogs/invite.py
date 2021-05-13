import discord
from discord.ext import commands, tasks
import traceback
import json
import os
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invkingupdate.start()

    async def getInvs(self): # Get JSON string of number of users each user invited in Discord channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798227110892273684)
        return json.loads(msg.content)

    async def updateInvs(self, dict): # Update JSON string of number of users each user invited in Discord channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798227110892273684)
        await msg.edit(content=json.dumps(dict, indent=4))

    @commands.Cog.listener()
    async def on_ready(self):
        global invites
        invites = {}
        guild = self.bot.get_guild(793495102566957096)
        invites[guild.id] = await guild.invites()
        print("Invites cached!")

    def code2inv(self, list, code):
        for invite in list:
            if invite.code == code:
                return invite
        else:
            return False

    def diff(self, li1: list, li2: list):
        return list(set(li2)-set(li1))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global invites
        if not member.bot:
            old_inv = invites[member.guild.id]
            new_inv = await member.guild.invites()
            for invite in old_inv:
                try:
                    if invite.uses < int(self.code2inv(new_inv, invite.code).uses): # Found the invite!
                        invites[member.guild.id] = new_inv
                        with open('invitechannel.json', 'r') as f:
                            invc = json.load(f)
                            channel = self.bot.get_channel(int(invc[str(member.guild.id)]))
                            embed=discord.Embed(title=f'{member.name} Joined!', color=0xff9000)
                            embed.add_field(name="Joined", value=f"<@{member.id}>", inline=True)
                            embed.add_field(name="Invited by", value=f"<@{invite.inviter.id}>", inline=True)
                            embed.add_field(name="Joined with link", value=f"https://discord.gg/{invite.code}", inline=False)
                        await channel.send(embed=embed)
                        bumps = await self.getInvs()
                        ## Update the JSON string
                        if str(invite.inviter.id) in bumps:
                            bumpno = int(bumps[str(invite.inviter.id)])
                            bumps[str(invite.inviter.id)] = int(bumpno + 1)
                        else:
                            bumps.update({f"{str(invite.inviter.id)}": 1})
                        await self.updateInvs(bumps)
                        return
                    elif not self.code2inv(new_inv, invite.code):
                        continue
                except AttributeError:
                    continue
            if len(self.diff(li1=old_inv, li2=new_inv)) > 0: # New invite link!
                invite = (self.diff(old_inv, new_inv))[0]
                invites[member.guild.id] = new_inv
                with open('invitechannel.json', 'r') as f:
                    invc = json.load(f)
                    channel = self.bot.get_channel(int(invc[str(member.guild.id)]))
                    embed=discord.Embed(title=f'{member.name} Joined!', color=0xff9000)
                    embed.add_field(name="Joined", value=f"<@{member.id}>", inline=True)
                    embed.add_field(name="Invited by", value=f"<@{invite.inviter.id}>", inline=True)
                    embed.add_field(name="Joined with link", value=f"https://discord.gg/{invite.code}", inline=False)
                await channel.send(embed=embed)
                bumps = await self.getInvs()
                ## Update JSON string
                if str(invite.inviter.id) in bumps:
                    bumpno = int(bumps[str(invite.inviter.id)])
                    bumps[str(invite.inviter.id)] = int(bumpno + 1)
                else:
                    bumps.update({f"{str(invite.inviter.id)}": 1})
                await self.updateInvs(bumps)

    @commands.command(aliases=["invleader"])
    async def inviteleaderboard(self, ctx):
        bumps = await self.getInvs()
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
        leaderv = list(leaders.values())
        leaderk = list(leaders.keys())
        msg = "**__Invites Leaderboard__**"
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
                msg += f"\n{str(place)}. {user.name}#{user.discriminator} - {rank} Invite"
                if int(bumpe) > 1:
                    msg += "s"
                usersDone += 1
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global invites
        try:
            invites[member.guild.id] = await member.guild.invites()
        except discord.errors.Forbidden as exception:
            traceback.print_exc()

    @commands.command()
    async def invitechannel(self, ctx, *, channel):
        owner = os.environ.get("OWNER")
        if str(ctx.author.id) == owner:
            with open('invitechannel.json', 'r') as f:
                invc = json.load(f)
            invc[ctx.guild.id] = channel.replace('<', '').replace('>', '').replace('#', '')
            with open('invitechannel.json', 'w') as f:
                json.dump(invc, f, indent=4)
            await ctx.send(f"`invc[{str(ctx.guild.id)}]` set to `{channel.replace('<', '').replace('>', '').replace('#', '')}`!")
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @commands.command()
    async def inviteremove(self, ctx):
        owner = os.environ.get("OWNER")
        if str(ctx.author.id) == owner:
            with open('invitechannel.json', 'r') as f:
                invc = json.load(f)
                invc.pop(ctx.guild.id)
            with open('invitechannel.json', 'w') as f:
                json.dump(invc, f, indent=4)
            await ctx.send('Removed invite channel!')
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @tasks.loop(seconds=30)
    async def invkingupdate(self):
        try:
            bumps = await self.getInvs()
            del bumps["302050872383242240"]
            bumpsRank = dict(sorted(bumps.items(), key=lambda item: item[1])) # Function to rank dictionary
            bumpKingValue = int(list(bumpsRank.values())[-1])
            guild = self.bot.get_guild(793495102566957096)
            bumpKing = get(guild.roles, id=797435990939009024)
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
            noice = "All hail the new Invite King"
            if len(addBumpKings) > 1:
                noice += "s"
            for user in addBumpKings:
                noice += f" <@{user.id}>"
            noice += "!"
            bumpChannel = self.bot.get_channel(793514694660194314)
            if len(addBumpKings) > 0:
                await bumpChannel.send(noice)
            for user in addBumpKings:
                await user.add_roles(bumpKing)
            for user in removeBumpKings:
                await user.remove_roles(bumpKing)
        except:
            traceback.print_exc()

    @invkingupdate.before_loop
    async def before_invkingupdate(self):
        await self.bot.wait_until_ready()
        
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="invleader",
                       description="Gives a leaderboard of invites",
                       guild_ids=[guildID])
    async def _invleader(self, ctx: SlashContext):
        bumps = await self.getInvs()
        leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
        leaderv = list(leaders.values())
        leaderk = list(leaders.keys())
        msg = "**__Invites Leaderboard__**"
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
                msg += f"\n{str(place)}. {user.name}#{user.discriminator} - {rank} Invite"
                if rank > 1:
                    msg += "s"
                usersDone += 1
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Invite(bot))
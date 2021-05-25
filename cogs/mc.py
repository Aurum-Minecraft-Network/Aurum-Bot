import discord
from discord.ext import commands
from discord.utils import get
import json
from decouple import config
import boto3
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="usernamereg")
    async def unr(self, ctx, version, *, username=None):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if version not in ["bedrock", "java"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only play on `bedrock` or `java`!", color=0x36393f)
            await ctx.send(embed=embed)
        elif username:
            if username.startswith("#") and version == "bedrock":
                username = username[1:]
            usernames = json.loads(client.get_object(Bucket="atpcitybot", Key="usernames.json")["Body"].read())
            ## Checking which entries exist
            if f"{str(ctx.author.id)}" in usernames:
                if version in usernames[str(ctx.author.id)]:
                    usernames[str(ctx.author.id)][version] = username
                else:
                    usernames[str(ctx.author.id)].update({f"{version}": f"{username}"})
            else:
                usernames.update({f"{str(ctx.author.id)}": {f"{version}": f"{username}"}})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "atpcitybot", "usernames.json")
            embed = discord.Embed(title=f"{get(emojis, name='success')} Registration Successful", description=f"Registered your {version.title()} username as **{username}**, <@{ctx.author.id}>.\n\nPro Tip: next time, try `/usernamereg`! Slash commands are available for this bot.", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="Your username is invalid!", color=0x36393f)
            await ctx.send(embed=embed)

    @commands.command(name="username")
    async def un(self, ctx, version, *, user: discord.User):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if version not in ["bedrock", "java"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only query a `bedrock` or `java` username!", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            usernames = json.loads(client.get_object(Bucket="atpcitybot", Key="usernames.json")["Body"].read())
            try:
                embed = discord.Embed(title=f"{get(emojis, name='usernamequery')} Minecraft username query", description=f"The {version.title()} username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)][version]}__**", color=0x36393f)
                await ctx.send(embed=embed)
            except KeyError:
                embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Username Not Registered", description="That user hasn't registered their username yet!", color=0x36393f)
                await ctx.send(embed=embed)
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if int(message.channel.id) == 808347566588035112:
            ## Chat check
            for i in message.content.splitlines():    
                if i.startswith("<"):
                    ## Command check
                    k = 0
                    for j in i.split(" "):
                        if ">" in j:
                            break # Left the username section
                        else:
                            k += 1
                            continue
                    if not i.split(" ")[k+1].startswith("/"):
                        channel = self.bot.get_channel(793645654324281376)
                        msg = i.replace("<", "", 1).replace(">", " »", 1)
                        await channel.send(f"**[BE]** {msg}")
            ## Join check
                elif i.endswith("joined the game"):
                    i = i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 3 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    i = " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** joined the Bedrock server")
                elif i.endswith("joined the game as op!"):
                    i = i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 5 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    i = " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** joined the Bedrock server")    
            ## Leave check
                elif i.endswith("left the game"):
                    i = i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 3 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    i = " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** left the Bedrock server")
                elif i.endswith("left the game as op!"):
                    i = i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 5 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    i = " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** left the Bedrock server")
            ## MCPEDiscordRelay enable check
                elif i == "MCPEDiscordRelay enabled":
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(":white_check_mark: **Bedrock Server has started**")
                    
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="usernamereg",
                       description="Register your Minecraft username",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="edition",
                               description="the Minecraft edition you want to register in",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="bedrock",
                                       value="bedrock"
                                   ),
                                   create_choice(
                                       name="java",
                                       value="java"
                                   )
                               ]
                           ),
                           create_option(
                               name="username",
                               description="the Minecraft username itself",
                               option_type=3,
                               required=True
                           )
                       ])
    async def _unr(self, ctx: SlashContext, version, username):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if version not in ["bedrock", "java"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only play on `bedrock` or `java`!", color=0x36393f)
            await ctx.send(embed=embed)
        elif username:
            await ctx.defer()
            if username.startswith("#") and version == "bedrock":
                username = username[1:]
            usernames = json.loads(client.get_object(Bucket="atpcitybot", Key="usernames.json")["Body"].read())
            ## Checking which entries exist
            if f"{str(ctx.author.id)}" in usernames:
                if version in usernames[str(ctx.author.id)]:
                    usernames[str(ctx.author.id)][version] = username
                else:
                    usernames[str(ctx.author.id)].update({f"{version}": f"{username}"})
            else:
                usernames.update({f"{str(ctx.author.id)}": {f"{version}": f"{username}"}})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "atpcitybot", "usernames.json")
            embed = discord.Embed(title=f"{get(emojis, name='success')} Registration Successful", description=f"Registered your {version.title()} username as **{username}**, <@{ctx.author.id}>.", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="Your username is invalid!", color=0x36393f)
            await ctx.send(embed=embed)
            
    @cog_ext.cog_slash(name="username",
                       description="Query a Minecraft username of a Discord user",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="edition",
                               description="the Minecraft edition of the username you want to query",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="bedrock",
                                       value="bedrock"
                                   ),
                                   create_choice(
                                       name="java",
                                       value="java"
                                   )
                               ]
                           ),
                           create_option(
                               name="user",
                               description="the Discord user you want to query",
                               option_type=6,
                               required=True
                           )
                       ])
    async def _un(self, ctx: SlashContext, version, user: discord.User):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if version not in ["bedrock", "java"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only query a `bedrock` or `java` username!", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            await ctx.defer()
            usernames = json.loads(client.get_object(Bucket="atpcitybot", Key="usernames.json")["Body"].read())
            try:
                embed = discord.Embed(title=f"{get(emojis, name='usernamequery')} Minecraft username query", description=f"The {version.title()} username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)][version]}__**", color=0x36393f)
                await ctx.send(embed=embed)
            except KeyError:
                embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Username Not Registered", description="That user hasn't registered their username yet!", color=0x36393f)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))

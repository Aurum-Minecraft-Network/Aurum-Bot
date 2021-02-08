import discord
from discord.ext import commands
import json
from decouple import config
import boto3

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="usernamereg")
    async def unr(self, ctx, version, *, username=None):
        if version not in ["bedrock", "java"]:
            await ctx.send("You can only play on `bedrock` or `java`!")
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
            await ctx.send(f"Registered your {version.title()} username as **{username}**, <@{ctx.author.id}>.")
        else:
            await ctx.send("Your username is invalid!")

    @commands.command(name="username")
    async def un(self, ctx, version, *, user: discord.User):
        if version not in ["bedrock", "java"]:
            await ctx.send("You can only query a `bedrock` or `java` username")
        else:
            usernames = json.loads(client.get_object(Bucket="atpcitybot", Key="usernames.json")["Body"].read())
            try:
                await ctx.send(f"The {version.title()} username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)][version]}__**")
            except KeyError:
                await ctx.send("That user hasn't registered their username yet!")
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if int(message.channel.id) == 808347566588035112:
            ## Chat check
            for i in message.content.splitlines():
                if i.startswith("<"):
                    channel = self.bot.get_channel(793645654324281376)
                    msg = i.replace("<", "").replace(">", " »")
                    await channel.send(f"**[BE]** {msg}")
            ## Join check
                elif i.endswith("joined the game"):
                    i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 3 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** joined the server")
            ## Leave check
                elif i.endswith("left the game"):
                    i.replace("[Server thread/INFO]: ", "")
                    i = i.split(" ")
                    del i[0]
                    ## Delete the last 3 items
                    del i[-1]
                    del i[-1]
                    del i[-1]
                    " ".join(i) # Got the username!
                    channel = self.bot.get_channel(793645654324281376)
                    await channel.send(f"**{i}** left the server")

def setup(bot):
    bot.add_cog(Minecraft(bot))

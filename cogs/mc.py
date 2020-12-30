import discord
from discord.ext import commands
import json

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="usernamereg")
    async def unr(self, ctx, version, *, username=None):
        if version not in ["bedrock", "java"]:
            await ctx.send("You can only play on `bedrock` or `java`!")
        elif username:
            with open("usernames.json", "r") as f:
                usernames = json.load(f)
            usernames.update({f"{str(ctx.author.id)}": {f"{version}": f"{username}"}})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            await ctx.send(f"Registered your {version.title()} username as {username}, <@{ctx.author.id}>.")
        else:
            await ctx.send("Your username is invalid!")

    @commands.command(name="username")
    async def un(self, ctx, version, *, user: discord.User):
        if version not in ["bedrock", "java"]:
            await ctx.send("You can only query a `bedrock` or `java` username")
        else:
            with open("usernames.json", "r") as f:
                usernames = json.load(f)
            try:
                await ctx.send(f"The {version.title()} username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)][version]}__**")
            except KeyError:
                await ctx.send("That user hasn't registered their username yet!")

def setup(bot):
    bot.add_cog(Minecraft(bot))

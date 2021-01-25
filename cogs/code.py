import discord
from discord.ext import commands
import json

class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def genMne(self, num: int):
        dig = str(bin(num)[2:])
        addDig = len(dig)
        addDig -= addDig % -11
        dig = "0" * (addDig - len(dig)) + dig
        indices = [dig[i:i+11] for i in range(0, len(dig), 11)]
        words = ""
        with open("assets/wordlist.json", "r") as f:
            wordList = json.load(f)
        for index in indices:
            index = int(index, 2)
            words += wordList[index] + " "
        return words

    @commands.command(name="genMne")
    async def x(self, ctx, user: discord.User=None):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Please use this command at a DM!")
        elif not user:
            await ctx.send(self.genMne(int(ctx.author.id)))
        elif user and str(ctx.author.id) == "438298127225847810":
            await ctx.send(self.genMne(int(user.id)))

def setup(bot):
    bot.add_cog(Code(bot))

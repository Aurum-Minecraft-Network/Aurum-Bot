import discord
from discord.ext import commands
import jsoncomment as json

class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def genMne(self, num: int):
        dig = str(bin(num)[2:]) # The User ID is converted to binary then to a string.
        addDig = len(dig)
        addDig -= addDig % -11 # How many 0's to add until len(dig) % 11 == 0
        dig = "0" * (addDig - len(dig)) + dig # 0's are added in to make the length of the string divisible to 11.
        indices = [dig[i:i+11] for i in range(0, len(dig), 11)] # The string is split into 11-character sections.
        words = ""
        with open("assets/wordlist.jsonc", "r") as f: 
            wordList = json.load(f) # 2^11 = 2048, so each section has a value from 0 to 2047.
        for index in indices:
            index = int(index, 2) # Convert the binary string back to an integer.
            words += wordList[index] + " " # Take the word based on the index.
        return words

    @commands.command(name="genMne")
    async def x(self, ctx, user: discord.User=None):
        if not isinstance(ctx.channel, discord.channel.DMChannel) and str(ctx.author.id) != "438298127225847810":
            await ctx.send("Please use this command at a DM!")
        elif not user:
            await ctx.send(f"Here is your mnemonic code:```\n{self.genMne(int(ctx.author.id))}```")
        elif user and str(ctx.author.id) == "438298127225847810":
            await ctx.send(f"```\n{self.genMne(int(user.id))}\n```")

def setup(bot):
    bot.add_cog(Code(bot))

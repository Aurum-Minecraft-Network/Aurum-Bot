import discord
from discord.ext import commands


class AddUpDownVote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 828240711144570911:
            return
        await message.add_reaction("<:upvote:828242926643445771>")
        await message.add_reaction("<:downvote:828242926672281660>")


def setup(bot):
    bot.add_cog(AddUpDownVote(bot))

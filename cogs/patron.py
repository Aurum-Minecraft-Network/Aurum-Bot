import discord
from discord.ext import commands, tasks
from discord.utils import get

class Patron(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boostCheck.start()

    @tasks.loop(minutes=1)
    async def boostCheck(self):
        guild = self.bot.get_guild(793495102566957096)
        role = get(guild.roles, id=799540153780928514)
        role2 = get(guild.roles, id=813406209486487583)
        for member in guild.members:
            if role in member.roles:
                await member.add_roles(role2)
                
    @boostCheck.before_loop
    async def before_boostCheck(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Patron(bot))
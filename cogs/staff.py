import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import uuid

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uuid")
    @has_permissions(administrator=True)
    async def gen_uuid(self, ctx):
        await ctx.send(str(uuid.uuid4()))
        
    @gen_uuid.error
    async def gen_uuid_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

def setup(bot):
    bot.add_cog(Staff(bot))

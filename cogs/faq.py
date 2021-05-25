import discord
from discord.ext import commands
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.utils import get

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx, index=None):
        emojis = self.bot.get_guild(846318304289488906).emojis
        with open("assets/faq.json", "r", encoding="utf-8") as f:
            faqs = json.load(f)
        if not index:
            msg = ""
            for index, entry in enumerate(faqs):
                msg += f"""**{entry["name"]}** - `{index + 1}`\n"""
            embed = discord.Embed(title=f"{get(emojis, name='faq')} FAQ: List of entries", description="Use `a!faq [number]` to get more help.\n\n" + msg, color=0x36393f)
            await ctx.send(embed=embed)
        else:
            try:
                entry = faqs[int(index) - 1]
                embed = discord.Embed(title=f"{get(emojis, name='faq')} FAQ {index}", description=f"**Question:** {entry['name']}\n\n**Answer:** {entry['value']}", color=0x36393f)
                await ctx.send(embed=embed)
            except IndexError:
                embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Index Out Of Range", description=f"The number you gave is out of range! Please give a number between `1` and `{len(faqs)}`!", color=0x36393f)
                await ctx.send(embed=embed)
                
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="faq",
                       description="Returns a list of frequently asked questions",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="entry",
                               description="The index of the FAQ",
                               option_type=4,
                               required=False
                           )
                       ])
    async def _faq(self, ctx: SlashContext, index=None):
        emojis = self.bot.get_guild(846318304289488906).emojis
        with open("assets/faq.json", "r", encoding="utf-8") as f:
            faqs = json.load(f)
        if not index:
            msg = ""
            for index, entry in enumerate(faqs):
                msg += f"""**{entry["name"]}** - `{index + 1}`\n"""
            embed = discord.Embed(title=f"{get(emojis, name='faq')} FAQ: List of entries", description="Use `a!faq [number]` to get more help.\n\n" + msg, color=0x36393f)
            await ctx.send(embed=embed)
        else:
            try:
                entry = faqs[int(index) - 1]
                embed = discord.Embed(title=f"{get(emojis, name='faq')} FAQ {index}", description=f"**Question:** {entry['name']}\n\n**Answer:** {entry['value']}", color=0x36393f)
                await ctx.send(embed=embed)
            except IndexError:
                embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Index Out Of Range", description=f"The number you gave is out of range! Please give a number between `1` and `{len(faqs)}`!", color=0x36393f)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FAQ(bot))

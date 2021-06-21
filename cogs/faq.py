import discord
from discord.ext import commands
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.utils import get
import datetime


class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx, index=None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        with open("assets/faq.json", "r", encoding="utf-8") as f:
            faqs = json.load(f)
        if not index:
            msg = ""
            for index, entry in enumerate(faqs):
                msg += f"""**{entry["name"]}** - `{index + 1}`\n"""
            title = (
                f"{get(emojis, name='faq')} " if get_icons()[str(ctx.author.id)] else ""
            )
            title += "FAQ: List of entries"
            embed = discord.Embed(
                title=title,
                description="Use `a!faq [number]` to get more help.\n\n" + msg,
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            if not get_design()[str(ctx.author.id)]:
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.avatar_url,
                )
                embed.set_footer(
                    text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                )
            await ctx.send(embed=embed)
        else:
            try:
                entry = faqs[int(index) - 1]
                title = (
                    f"{get(emojis, name='faq')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += f"FAQ: {index}"
                embed = discord.Embed(
                    title=title,
                    description=f"**Question:** {entry['name']}\n\n**Answer:** {entry['value']}",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                if not get_design()[str(ctx.author.id)]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)
            except IndexError:
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Error: Index Out Of Range"
                embed = discord.Embed(
                    title=title,
                    description=f"The number you gave is out of range! Please give a number between `1` and `{len(faqs)}`!",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                if not get_design()[str(ctx.author.id)]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)

    ### SLASH COMMANDS ZONE ###

    guildID = 793495102566957096

    @cog_ext.cog_slash(
        name="faq",
        description="Returns a list of frequently asked questions",
        guild_ids=[guildID],
        options=[
            create_option(
                name="entry",
                description="The index of the FAQ",
                option_type=4,
                required=False,
            )
        ],
    )
    async def _faq(self, ctx: SlashContext, index=None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        with open("assets/faq.json", "r", encoding="utf-8") as f:
            faqs = json.load(f)
        if not index:
            msg = ""
            for index, entry in enumerate(faqs):
                msg += f"""**{entry["name"]}** - `{index + 1}`\n"""
            title = (
                f"{get(emojis, name='faq')} " if get_icons()[str(ctx.author.id)] else ""
            )
            title += "FAQ: List of entries"
            embed = discord.Embed(
                title=title,
                description="Use `a!faq [number]` to get more help.\n\n" + msg,
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            if not get_design()[str(ctx.author.id)]:
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.avatar_url,
                )
                embed.set_footer(
                    text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                )
            await ctx.send(embed=embed)
        else:
            try:
                entry = faqs[int(index) - 1]
                title = (
                    f"{get(emojis, name='faq')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += f"FAQ: {index}"
                embed = discord.Embed(
                    title=title,
                    description=f"**Question:** {entry['name']}\n\n**Answer:** {entry['value']}",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                if not get_design()[str(ctx.author.id)]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)
            except IndexError:
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Error: Index Out Of Range"
                embed = discord.Embed(
                    title=title,
                    description=f"The number you gave is out of range! Please give a number between `1` and `{len(faqs)}`!",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                if not get_design()[str(ctx.author.id)]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FAQ(bot))

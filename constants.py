# For bot token; AWS details and ImgurAPI details, set them in .env (environment variables), not here.


### Magic Numbers
# These numbers should not be modified if you don't know what you are doing!

## Server IDs

AURUM_ASSET_SERVER_ID = 846318304289488906
AURUM_MAIN_SERVER_ID = 793495102566957096

## Channel IDs

WELCOME_GOODBYE_CHANNEL_ID = 793513021288742912
RULES_CHANNEL_ID = 793529403233665084
HOW_TO_JOIN_CHANNEL_ID = 793513974582607962
SELF_ASSIGN_ROLES_CHANNEL_ID = 793626862180892732

## Role IDs

EVERYBODY_ROLE_ID = 833003253859221505

### Other constants
# Do not modify these constants if you don't know what you are doing!

BOT_DEV = (438298127225847810, 383961317280841730, 353168066466545664, 507267673348898824)

### Commands to update constants

import datetime
import discord
from discord.ext import commands
from typing import Union
from discord.utils import get
from discord_slash.context import SlashContext
import traceback

class CogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def send_no_permission(
        self,
        ctx: Union[
            discord.ext.commands.Context,
            SlashContext,
            discord.TextChannel,
            discord.DMChannel,
            discord.GroupChannel,
        ],
    ):
        from cogs.aesthetics import design, embedColor, icons
        emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
        title += "Error: No Permission"
        embed = discord.Embed(
            title=title,
            description="Sorry, but you don't have permission to do that.",
            color=int(embedColor[ctx.author.id], 16),
        )
        if not design[ctx.author.id]:
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_footer(
                text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def constant(self, ctx, var_type: str, var_name: str, value: Union[str, int, float, dict, list, tuple, set]):
        from cogs.aesthetics import design, embedColor, icons
        emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        if ctx.author.id in BOT_DEV:
            if var_type not in ["binInt", "octInt", "hexInt", "str", "int", "float", "dict", "list", "tuple", "set"]:
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "Error: Invalid Parameter"
                embed = discord.Embed(
                    title=title,
                    description="`var_type` may only be one of: `binInt`, `octInt`, `hexInt`, `str`, `int`, `float`, `dict`, `list`, `tuple`, `set`",
                    color=int(embedColor[ctx.author.id], 16),
                )
                if not design[ctx.author.id]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)
                return
            try:
                if var_type == "binInt":
                    exec(f"global {var_name}\n{var_name} = int({value}, 2)")
                elif var_type == "octInt":
                    exec(f"global {var_name}\n{var_name} = int({value}, 8)")
                elif var_type == "hexInt":
                    exec(f"global {var_name}\n{var_name} = int({value}, 16)")
                elif var_type in ["str", "int", "float", "dict", "list", "tuple", "set"]:
                    exec(f"global {var_name}\n{var_name} = {var_type}({value})")
            except:
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "An Exception Occured!"
                embed = discord.Embed(
                    title=title,
                    description=traceback.format_exc(),
                    color=int(embedColor[ctx.author.id], 16),
                )
                if not design[ctx.author.id]:
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
                title = f"{get(emojis, name='dev')} " if icons[ctx.author.id] else ""
                title += "Constant Value Change"
                embed = discord.Embed(
                    title=title,
                    description=f"{var_name} has been changed to {value}.",
                    color=int(embedColor[ctx.author.id], 16),
                )
                if not design[ctx.author.id]:
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
            await self.send_no_permission(ctx=ctx)

def setup(bot):
    bot.add_cog(CogName(bot))

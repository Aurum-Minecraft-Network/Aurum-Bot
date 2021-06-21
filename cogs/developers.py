from typing import Union
import discord
from discord.ext import commands
from discord.utils import get
from disputils import BotEmbedPaginator
import discord_slash
import sys
import io
import traceback
import datetime
from constants import BOT_DEV, AURUM_ASSET_SERVER_ID


class Developers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_no_permission(
        self,
        ctx: Union[
            discord.ext.commands.Context,
            discord_slash.SlashContext,
            discord.TextChannel,
            discord.DMChannel,
            discord.GroupChannel,
        ],
    ):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        title = (
            f"{get(emojis, name='error')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Error: No Permission"
        embed = discord.Embed(
            title=title,
            description="Sorry, but you don't have permission to do that.",
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

    @commands.command()
    async def send(self, ctx, *, content):
        if ctx.author.id not in BOT_DEV:
            await self.send_no_permission(ctx=ctx)
            return
        await ctx.send(content)

    @commands.command(name="exec")
    async def exec_command(self, ctx, *, arg1):
        """(botdev only) Runs python code in code block and returns errors if the code has errors"""
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        if ctx.author.id in BOT_DEV:
            arg1 = arg1[6:-4]
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            try:
                exec(arg1)
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
            except:
                x = traceback.format_exc()
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "An Exception Occured!"
                embed = discord.Embed(
                    title=title, color=int(get_embedColor()[str(ctx.author.id)], 16)
                )
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Code", value=f"```py\n{str(arg1)}\n```", inline=False
                )
                embed.add_field(
                    name="Output", value=f"```\n{str(x)}\n```", inline=False
                )
                await ctx.send(embed=embed)
            else:
                title = (
                    f"{get(emojis, name='success')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Execution Successful"
                embed = discord.Embed(
                    title=f"Execution Success!",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Code", value=f"```py\n{str(arg1)}\n```", inline=False
                )
                embed.add_field(
                    name="Output", value=f"```\n{str(output)}\n```", inline=False
                )
            finally:
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
            await self.send_no_permission(ctx=ctx)

    @commands.command(name="asyncDef")
    async def async_def_command(self, ctx, *, arg1):
        """(botdev only) Defines async function and returns error if it fails"""
        if ctx.author.id in BOT_DEV:
            arg1 = arg1[6:-4]
            try:
                func = "global asyncExec\nasync def asyncExec():\n"
                ## Indent each line of arg1 by 4 spaces
                for line in iter(arg1.splitlines()):
                    func += "    " + line + "\n"
                exec(func)
            except:
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "An Exception Occured!"
                embed = discord.Embed(
                    title=title, color=int(get_embedColor()[str(ctx.author.id)], 16)
                )
                embed.add_field(
                    name="Input", value=f"```py\n{str(arg1)}\n```", inline=False
                )
                embed.add_field(
                    name="Output",
                    value=f"```\n{str(traceback.format_exc())}\n```",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "An Exception Occured!"
                embed = discord.Embed(
                    title=f"Definition Success!",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                embed.add_field(
                    name="Definition Successful",
                    value=f"```py\n{str(func)}\n```",
                    inline=False,
                )
            finally:
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
            await self.send_no_permission(ctx=ctx)

    @commands.command(name="asyncExec")
    async def async_exec_command(self, ctx):
        """(botdev) Runs async command and returns error if it fails"""
        if ctx.author.id in BOT_DEV:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            try:
                global asyncExec
                await asyncExec()  # Ignore this error in your linter; asyncExec will be defined in async_def_command.
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
                del asyncExec  # Ignore this error in your linter; asyncExec will be defined in async_def_command.
            except:
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "An Exception Occured!"
                embed = discord.Embed(
                    title=title, color=int(get_embedColor()[str(ctx.author.id)], 16)
                )
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Output",
                    value=f"```\n{str(traceback.format_exc())}\n```",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='dev')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Execution successful"
                embed = discord.Embed(
                    title=title, color=int(get_embedColor()[str(ctx.author.id)], 16)
                )
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Output",
                    value=f"```\n{str(traceback.format_exc())}\n```",
                    inline=False,
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    title=f"Execution Success!",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Output", value=f"```\n{str(output)}\n```", inline=False
                )
                await ctx.send(embed=embed)
            finally:
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
            await self.send_no_permission(ctx=ctx)

    @commands.command()
    async def devhelp(self, ctx):
        if ctx.author.id in BOT_DEV:
            emojis = self.bot.get_guild(846318304289488906).emojis
            from cogs.aesthetics import get_design, get_embedColor, get_icons

            if get_design()[str(ctx.author.id)]:
                title = (
                    f"{get(emojis, name='help')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Aurum Bot Debugging Guide"
                embed1 = discord.Embed(
                    title=title,
                    description=f"""{get(emojis, name="bump")} `a!bumpreset [true|false](boolean)`
<:space:846393726586191923> Resets the bump status. Note that this does not affect DISBOARD.

{get(emojis, name="async")} `a!asyncDef [code](string)`
<:space:846393726586191923> Defines an asynchronous function `asyncDef`. Start `code` with 3 backticks, then `py`, then a new line, then the code. Add a new line, then input 3 backticks to enclose the code.

{get(emojis, name="async")} `a!asyncExec`
<:space:846393726586191923> Executes the asynchronous function `asyncDef`.

{get(emojis, name="dev")} `a!exec [code](string)`
<:space:846393726586191923> Executes Python code. Recommended over `a!asyncDef` and `a!asyncExec` when no asynchronous functions are needed. Start `code` with 3 backticks, then `py`, then a new line, then the code. Add a new line, then input 3 backticks to enclose the code.

{get(emojis, name="async")} `a!sync_members`
<:space:846393726586191923> Adds missing entries to the files `design.json`, `embedColor.json`, and `icons.json`.""",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )

                embed2 = discord.Embed(
                    title=title,
                    description=f"""{get(emojis, name="extload")} `a!extload [cog](string)`
<:space:846393726586191923> Loads an extension (cog).

{get(emojis, name="extload")} `a!extloadall`
<:space:846393726586191923> Loads every extension (cog).

{get(emojis, name="extunload")} `a!extunload [cog](string)`
<:space:846393726586191923> Unloads an extension (cog).

{get(emojis, name="extreload")} `a!extreload [cog](string)`
<:space:846393726586191923> Reloads an extension (cog). Equivalent to running `a!extunload` then `a!extload`.

{get(emojis, name="extlist")} `a!extlist`
<:space:846393726586191923> Lists all extension (cog) names.""",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )

                embed1.set_footer(text="[] Required {} Optional")
                embed2.set_footer(text="[] Required {} Optional")
                embeds = [embed1, embed2]
                paginator = BotEmbedPaginator(ctx, embeds)
                await paginator.run()
            else:
                title = (
                    f"{get(emojis, name='help')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Aurum Bot Debugging Guide"
                embed1 = discord.Embed(
                    title=title,
                    description="Following is a list of commands for debugging only.",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                embed2 = discord.Embed(
                    title=title,
                    description="Following is a list of commands for debugging only.",
                    color=int(get_embedColor()[str(ctx.author.id)], 16),
                )
                embed1.add_field(
                    name="a!bumpreset [true|false](boolean)",
                    value="Resets the bump status. Note that this does not affect DISBOARD.",
                    inline=False,
                )
                embed1.add_field(
                    name="a!asyncDef [code](string)",
                    value="Defines an asynchronous function `asyncDef`. Start `code` with 3 backticks, then `py`, then a new line, then the code. Add a new line, then input 3 backticks to enclose the code.",
                    inline=False,
                )
                embed1.add_field(
                    name="a!asyncExec",
                    value="Executes the asynchronous function `asyncDef`.",
                    inline=False,
                )
                embed1.add_field(
                    name="a!exec [code](string)",
                    value="Executes Python code. Recommended over `a!asyncDef` and `a!asyncExec` when no asynchronous functions are needed. Start `code` with 3 backticks, then `py`, then a new line, then the code. Add a new line, then input 3 backticks to enclose the code.",
                    inline=False,
                )
                embed1.add_field(
                    name="a!sync_members",
                    value="Adds missing entries to the files `design.json`, `embedColor.json`, and `icons.json`.",
                    inline=False,
                )
                embed2.add_field(
                    name="a!extload [cog](string)",
                    value="Loads an extension (cog).",
                    inline=False,
                )
                embed2.add_field(
                    name="a!extloadall",
                    value="Loads every extension (cog).",
                    inline=False,
                )
                embed2.add_field(
                    name="a!extunload [cog](string)",
                    value="Unloads an extension (cog).",
                    inline=False,
                )
                embed2.add_field(
                    name="a!extreload [cog](string)",
                    value="Reloads an extension (cog). Equivalent to running `a!extunload` then `a!extload`.",
                    inline=False,
                )
                embed2.add_field(
                    name="a!extlist",
                    value="Lists all extension (cog) names.",
                    inline=False,
                )
                embed1.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
                embed2.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
                embed1.timestamp = datetime.datetime.utcnow()
                embed1.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.avatar_url,
                )
                embed1.set_footer(
                    text="[] Required {} Optional | Aurum Bot",
                    icon_url="https://i.imgur.com/sePqvZX.png",
                )
                embed2.timestamp = datetime.datetime.utcnow()
                embed2.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.avatar_url,
                )
                embed2.set_footer(
                    text="[] Required {} Optional | Aurum Bot",
                    icon_url="https://i.imgur.com/sePqvZX.png",
                )

                embeds = [embed1, embed2]
                paginator = BotEmbedPaginator(ctx, embeds)
                await paginator.run()
        else:
            await self.send_no_permission(ctx=ctx)


def setup(bot):
    bot.add_cog(Developers(bot))

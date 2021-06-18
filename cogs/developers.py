from typing import Union
import discord
from discord.ext import commands
from discord.utils import get
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
    async def send(self, ctx, *, content):
        if ctx.author.id not in BOT_DEV:
            await self.send_no_permission(ctx=ctx)
            return
        await ctx.send(content)
        
    @commands.command(name="exec")
    async def exec_command(self, ctx, *, arg1):
        from cogs.aesthetics import design, embedColor, icons
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
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "An Exception Occured!"
                embed = discord.Embed(title=title, color=int(embedColor[ctx.author.id], 16))
                embed.set_author(name="Aurum Bot")
                embed.add_field(name="Code", value=f"```py\n{str(arg1)}\n```", inline=False)
                embed.add_field(name="Output", value=f"```\n{str(x)}\n```", inline=False)
                await ctx.send(embed=embed)
            else:
                title = f"{get(emojis, name='success')} " if icons[ctx.author.id] else ""
                title += "Execution Successful"
                embed = discord.Embed(title=f"Execution Success!", color=int(embedColor[ctx.author.id], 16))
                embed.set_author(name="Aurum Bot")
                embed.add_field(name="Code", value=f"```py\n{str(arg1)}\n```", inline=False)
                embed.add_field(
                    name="Output", value=f"```\n{str(output)}\n```", inline=False
                )
            finally:
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


    @commands.command(name="asyncDef")
    async def async_def_command(self, ctx, *, arg1):
        if ctx.author.id in BOT_DEV:
            arg1 = arg1[6:-4]
            try:
                func = "global asyncExec\nasync def asyncExec():\n"
                ## Indent each line of arg1 by 4 spaces
                for line in iter(arg1.splitlines()):
                    func += "    " + line + "\n"
                exec(func)
            except:
                from cogs.aesthetics import design, embedColor, icons
                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "An Exception Occured!"
                embed = discord.Embed(title=title, color=int(embedColor[ctx.author.id], 16))
                embed.add_field(
                    name="Input", value=f"```py\n{str(arg1)}\n```", inline=False
                )
                embed.add_field(name="Output", value=f"```\n{str(traceback.format_exc())}\n```", inline=False)
                await ctx.send(embed=embed)
            else:
                from cogs.aesthetics import design, embedColor, icons
                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "An Exception Occured!"
                embed = discord.Embed(title=f"Definition Success!", color=int(embedColor[ctx.author.id], 16))
                embed.add_field(
                    name="Definition Successful",
                    value=f"```py\n{str(func)}\n```",
                    inline=False,
                )
            finally:
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


    @commands.command(name="asyncExec")
    async def async_exec_command(self, ctx):
        if ctx.author.id in BOT_DEV:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            try:
                global asyncExec
                await asyncExec() # Ignore this error in your linter; asyncExec will be defined in async_def_command.
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
                del asyncExec # Ignore this error in your linter; asyncExec will be defined in async_def_command.
            except:
                from cogs.aesthetics import design, embedColor, icons
                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "An Exception Occured!"
                embed = discord.Embed(title=title, color=int(embedColor[ctx.author.id], 16))
                embed.set_author(name="Aurum Bot")
                embed.add_field(name="Output", value=f"```\n{str(traceback.format_exc())}\n```", inline=False)
                await ctx.send(embed=embed)
            else:
                from cogs.aesthetics import design, embedColor, icons
                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = f"{get(emojis, name='dev')} " if icons[ctx.author.id] else ""
                title += "Execution successful"
                embed = discord.Embed(title=title, color=int(embedColor[ctx.author.id], 16))
                embed.set_author(name="Aurum Bot")
                embed.add_field(name="Output", value=f"```\n{str(traceback.format_exc())}\n```", inline=False)
                await ctx.send(embed=embed)
                embed = discord.Embed(title=f"Execution Success!", color=int(embedColor[ctx.author.id], 16))
                embed.set_author(name="Aurum Bot")
                embed.add_field(
                    name="Output", value=f"```\n{str(output)}\n```", inline=False
                )
                await ctx.send(embed=embed)
            finally:
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
    bot.add_cog(Developers(bot))

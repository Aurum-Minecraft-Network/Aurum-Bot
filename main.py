import discord
import os
import sys
import io
import traceback
from decouple import config
from discord.ext import commands, tasks
from discord.utils import get
from discord_components import DiscordComponents
import difflib
import discord_slash
from discord_slash.utils import manage_commands
from disputils import BotEmbedPaginator
from typing import Union
from constants import *
import datetime

global PREFIX
PREFIX = "a!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command("help")

# returns error message of person not having permission
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


# checking if bot is ready
@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="try my slash commands!"))
    print("We have logged in as {0.user}. Bot is ready.".format(bot))
    global aliases
    aliases = []
    for command in bot.commands:
        aliases += list(command.aliases) + [command.name]


# sends welcome message in the #welcome-goodbye channel when a member joins
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
    if member.guild.id != AURUM_MAIN_SERVER_ID:
        return
    await channel.send("<:oslash:803836347097677844>")
    await channel.send(
        f"<@{member.id}> has joined the server. Welcome, <@{member.id}>.\nRefer to <#{RULES_CHANNEL_ID}> for rules and <#{HOW_TO_JOIN_CHANNEL_ID}> for joining instructions.\nUse <#{SELF_ASSIGN_ROLES_CHANNEL_ID}> to assign some roles for yourself.\nNeed help? Use `/faq`!"
    )


# sends farewell message in the #welcome-goodbye channel when a member leaves
@bot.event
async def on_member_remove(member):
    if member.guild.id != AURUM_MAIN_SERVER_ID:
        return
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
    await channel.send(
        f"**{member.name}#{member.discriminator}** has left the server. Farewell, **{member.name}#{member.discriminator}**."
    )


## Message edit detection
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.event
async def on_command_error(ctx, error):
    triedCommand = ctx.message.content.split(" ")[0][2:]
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        try:
            closest = difflib.get_close_matches(triedCommand, aliases)[0]
            emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
            from cogs.aesthetics import design, embedColor, icons
            title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
            title += "Error: Invalid Command"
            embed = discord.Embed(
                title=title,
                description=f"Use `a!help` if you need help.\nDid you mean `a!{closest}`?",
                color=int(embedColor[ctx.author.id], 16),
            )
            await ctx.send(embed=embed)
        except IndexError:
            emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
            from cogs.aesthetics import design, embedColor, icons
            title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
            title += "Error: Invalid Command"
            embed = discord.Embed(
                title=title,
                description=f"Use `a!help` if you need help.",
                color=int(embedColor[ctx.author.id], 16),
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


@bot.command(name="extload")
async def ext_load(ctx, cog):
    if ctx.author.id in BOT_DEV:
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded extension `{cog}`!")
    else:
        await send_no_permission(ctx=ctx)


@bot.command(name="extunload")
async def ext_unload(ctx, cog):
    if ctx.author.id in BOT_DEV:
        bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded extension `{cog}`!")
    else:
        await send_no_permission(ctx=ctx)


@bot.command(name="extreload")
async def ext_reload(ctx, cog):
    if ctx.author.id in BOT_DEV:
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded extension `{cog}`!")
    else:
        await send_no_permission(ctx=ctx)


@bot.command(name="extlist")
async def ext_list(ctx):
    if ctx.author.id in BOT_DEV:
        exts = []
        for i in os.listdir("./cogs"):
            if i.endswith(".py"):
                exts.append(i[:-3])
        message1 = ""
        for j in exts:
            message1 += f"""`{j}`\n"""
        await ctx.send(message1)
    else:
        await send_no_permission(ctx=ctx)


@bot.command(name="extloadall")
async def ext_load_all(ctx):
    if ctx.author.id not in BOT_DEV:
        await send_no_permission(ctx=ctx)
        return
    for i in os.listdir("./cogs"):
        if i.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{i[:-3]}")
                await ctx.send(f"Loaded {i[:-3]}")
            except discord.ext.commands.errors.ExtensionNotFound:
                await ctx.send(f"Can't load {i[:-3]}")
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                await ctx.send(f"Already loaded {i[:-3]}")


@tasks.loop(minutes=1)
async def deny_dank_access():
    guild = bot.get_guild(793495102566957096)
    dank = guild.get_member(270904126974590976)
    dankRole = get(guild.roles, id=837999253947023371)
    for channel in guild.channels():
        if channel.id in [837715004991340555, 793520621417791539]:
            return
        channel.set_permissions(dank, read_messages=False, send_messages=False)
        channel.set_permissions(dankRole, read_messages=False, send_messages=False)


@bot.command()
async def ping(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(
        title=f"{get(emojis, name='ping')} Ping",
        description=f"**{round(bot.latency * 1000)}ms**",
        color=0x36393F,
    )
    await ctx.send(embed=embed)


@bot.command()
async def source(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(
        title=f"{get(emojis, name='source')} Source Code",
        description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot",
        color=0x36393F,
    )
    await ctx.send(embed=embed)


### SLASH COMMANDS ZONE ###

from discord_slash import SlashCommand

slash = SlashCommand(bot, sync_commands=True, override_type=True)

guildID = 793495102566957096


@slash.slash(name="ping", description="Returns the latency in ms", guild_ids=[guildID])
async def _ping(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(
        title=f"{get(emojis, name='ping')} Ping",
        description=f"**{round(bot.latency * 1000)}ms**",
        color=0x36393F,
    )
    await ctx.send(embed=embed)


@slash.slash(
    name="source", description="Returns the source code of the bot", guild_ids=[guildID]
)
async def _source(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(
        title=f"{get(emojis, name='source')} Source Code",
        description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot",
        color=0x36393F,
    )
    await ctx.send(embed=embed)


def run_bot():
    for i in os.listdir("./cogs"):
        if i.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{i[:-3]}")
            except discord.ext.commands.errors.ExtensionNotFound:
                pass
    print("Extensions loaded!")
    bot.run(config("TOKEN"))


run_bot()

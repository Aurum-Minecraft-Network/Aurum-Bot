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
from discord_slash.context import SlashContext
from typing import Union
from constants import (
    BOT_DEV,
    AURUM_ASSET_SERVER_ID,
    AURUM_MAIN_SERVER_ID,
    WELCOME_GOODBYE_CHANNEL_ID,
    RULES_CHANNEL_ID,
    HOW_TO_JOIN_CHANNEL_ID,
    SELF_ASSIGN_ROLES_CHANNEL_ID,
)
import datetime

PREFIX = "a!"
intents = discord.Intents.all()
<<<<<<< HEAD
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

token = config("TOKEN")
owner = config("OWNER")
botid = config("ID")

global botdev
botdev = str(owner)

# magic numbers
AURUM_ASSET_SERVER_ID=846318304289488906
AURUM_MAIN_SERVER_ID=793495102566957096
WELCOME_GOODBYE_CHANNEL_ID=793513021288742912
RULES_CHANNEL_ID=793529403233665084
HOW_TO_JOIN_CHANNEL_ID=793513974582607962
SELF_ASSIGN_ROLES_CHANNEL_ID=793626862180892732


async def sendNoPermission(ctx: Union[discord.ext.commands.Context, discord_slash.SlashContext, discord.TextChannel, discord.DMChannel, discord.GroupChannel]):
    """Returns error message of person not having permission"""
=======
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command("help")


async def send_no_permission(
    ctx: Union[
        discord.ext.commands.Context,
        SlashContext,
        discord.TextChannel,
        discord.DMChannel,
        discord.GroupChannel,
    ],
):
    """Returns error message of person not having permission"""
    from cogs.aesthetics import get_design, get_embedColor, get_icons

>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
    title = f"{get(emojis, name='error')} " if get_icons()[str(ctx.author.id)] else ""
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
        embed.set_footer(text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png")
    await ctx.send(embed=embed)

<<<<<<< HEAD
=======

# checking if bot is ready
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
@bot.event
async def on_ready():
    """Checks and prints message if bot is ready plus loading aliases"""
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="try my slash commands!"))
    print("We have logged in as {0.user}. Bot is ready.".format(bot))
    global aliases
    aliases = []
    for command in bot.commands:
        aliases += list(command.aliases) + [command.name]


<<<<<<< HEAD
=======
# sends welcome message in the #welcome-goodbye channel when a member joins
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
@bot.event
async def on_member_join(member):
    """Sends welcome message in the #welcome-goodbye channel when a member joins"""
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
    if member.guild.id != AURUM_MAIN_SERVER_ID:
        return
    await channel.send("<:oslash:803836347097677844>")
    await channel.send(
        f"<@{member.id}> has joined the server. Welcome, <@{member.id}>.\nRefer to <#{RULES_CHANNEL_ID}> for rules and <#{HOW_TO_JOIN_CHANNEL_ID}> for joining instructions.\nUse <#{SELF_ASSIGN_ROLES_CHANNEL_ID}> to assign some roles for yourself.\nNeed help? Use `/faq`!"
    )


<<<<<<< HEAD
=======
# sends farewell message in the #welcome-goodbye channel when a member leaves
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
@bot.event
async def on_member_remove(member):
    """Sends farewell message in the #welcome-goodbye channel when a member leaves"""
    if member.guild.id != AURUM_MAIN_SERVER_ID:
        return
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
<<<<<<< HEAD
    await channel.send(f"**{member.name}#{member.discriminator}** has left the server. Farewell, **{member.name}#{member.discriminator}**.")
    
=======
    await channel.send(
        f"**{member.name}#{member.discriminator}** has left the server. Farewell, **{member.name}#{member.discriminator}**."
    )


>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
@bot.event
async def on_message_edit(before, after):
    """Message edit detection"""
    await bot.process_commands(after)

<<<<<<< HEAD
=======

>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
@bot.event
async def on_command_error(ctx, error):
    """Attempts to find typo and inform the user. Returns normal error message if it fails"""
    triedCommand = ctx.message.content.split(" ")[0][2:]
<<<<<<< HEAD
    item_index = 1
    # If user added a space between prefix and command
    while len(triedCommand)==0:
        # loops until the tried message is the command
        triedCommand = ctx.message.content.split(" ")[item_index]
        item_index += 1
=======
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        try:
            closest = difflib.get_close_matches(triedCommand, aliases)[0]
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Command"
            embed = discord.Embed(
                title=title,
                description=f"Use `a!help` if you need help.\nDid you mean `a!{closest}`?",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
        except IndexError:
            emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
            from cogs.aesthetics import get_design, get_embedColor, get_icons

            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Command"
            embed = discord.Embed(
                title=title,
                description=f"Use `a!help` if you need help.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
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

<<<<<<< HEAD
@bot.command()
async def extload(ctx, cog):
    """(owner only) loads selected extension and returns error message when user has no permission"""
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
=======

@bot.command(name="extload")
async def ext_load(ctx, cog):
    """(devs only) loads selected extension and returns error message when user has no permission"""
    if ctx.author.id in BOT_DEV:
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded extension `{cog}`!")
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    else:
        await send_no_permission(ctx=ctx)

<<<<<<< HEAD
async def extunload(ctx, cog):
    """(owner only) Unloads selected extension"""
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
=======

@bot.command(name="extunload")
async def ext_unload(ctx, cog):
    """(devs only) Unloads selected extension"""
    if ctx.author.id in BOT_DEV:
        bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded extension `{cog}`!")
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    else:
        await send_no_permission(ctx=ctx)

<<<<<<< HEAD
@bot.command()
async def extreload(ctx, cog):
    """(owner only) Reloads selected extension"""
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
=======

@bot.command(name="extreload")
async def ext_reload(ctx, cog):
    """(devs only) Reloads selected extension"""
    if ctx.author.id in BOT_DEV:
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded extension `{cog}`!")
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    else:
        await send_no_permission(ctx=ctx)

<<<<<<< HEAD
@bot.command()
async def extlist(ctx):
    """(owner only) lists all extensions in the directory (even the ones that are not loaded)"""
    if str(ctx.author.id) == str(owner):
=======

@bot.command(name="extlist")
async def ext_list(ctx):
    if ctx.author.id in BOT_DEV:
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
        exts = []
        for i in os.listdir("./cogs"):
            if i.endswith(".py"):
                exts.append(i[:-3])
        message1 = ""
        for j in exts:
            message1 += f"""`{j}`\n"""
        await ctx.send(message1)
    else:
<<<<<<< HEAD
        await sendNoPermission(ctx=ctx)
    
@bot.command(name='exec')
async def exec_command(ctx, *, arg1):
    """(botdev only) Runs python code in code block and returns errors if the code has errors"""
    if str(ctx.author.id) == botdev:
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
            embed=discord.Embed(title=f'Execution Failed!', color=0xff0000)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await sendNoPermission(ctx=ctx)

@bot.command(name='asyncDef')
async def asyncDef_command(ctx, *, arg1):
    """(botdev only) Defines async function and returns error if it fails"""
    if str(ctx.author.id) == botdev:
        arg1 = arg1[6:-4]
        try:
            func = "global asyncExec\nasync def asyncExec():\n"
            ## Indent each line of arg1 by 4 spaces
            for line in iter(arg1.splitlines()):
                func += "    " + line + "\n"
            exec(func)
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Definition Failed!', color=0xff0000)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Input", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Definition Success!', color=0x00ff00)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Function Definition", value=f'```py\n{str(func)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await sendNoPermission(ctx=ctx)

@bot.command(name='asyncExec')
async def asyncExec_command(ctx):
    """(botdev) Runs async command and returns error if it fails"""
    if str(ctx.author.id) == botdev:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            global asyncExec
            await asyncExec()
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            del asyncExec
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Execution Failed!', color=0xff0000)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="Aurum Bot")
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await sendNoPermission(ctx=ctx)
        
@bot.command()
async def extLoadAll(ctx):
    """(botdev only) Loads all extensions"""
    if str(ctx.author.id) != botdev:
        await sendNoPermission(ctx=ctx)
=======
        await send_no_permission(ctx=ctx)


@bot.command(name="extloadall")
async def ext_load_all(ctx):
    if ctx.author.id not in BOT_DEV:
        await send_no_permission(ctx=ctx)
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
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
<<<<<<< HEAD
async def denyDankAccess():
=======
async def deny_dank_access():
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    """Returns not having dank memer permission error"""
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
<<<<<<< HEAD
    """Returns ping of the user"""
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
=======
    """Returns ping of the bot"""
    emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
    from cogs.aesthetics import get_design, get_embedColor, get_icons

    title = f"{get(emojis, name='ping')} " if get_icons()[str(ctx.author.id)] else ""
    title += "Ping"
    embed = discord.Embed(
        title=title,
        description=f"**{round(bot.latency * 1000)}ms**",
        color=int(get_embedColor()[str(ctx.author.id)], 16),
    )
    if not get_design()[str(ctx.author.id)]:
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_footer(text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png")
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    await ctx.send(embed=embed)


@bot.command()
async def source(ctx):
    """Sends message with the source code github page"""
<<<<<<< HEAD
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='source')} Source Code", description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot", color=0x36393f)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    """Shows helps menu"""
    # Format: {emoji} `full command` \n <space emoji> help text
    # TODO: Fix the UI
    emojis = bot.get_guild(846318304289488906).emojis
    embed1=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="ping")} `a!ping`
<:space:846393726586191923> Returns the latency in ms.

{get(emojis, name="menu")} `a!menu`
<:space:846393726586191923> Open the Navigation Menu.

{get(emojis, name="interview")} `a!interview`
<:space:846393726586191923> Initiate the Interview Wizard.

{get(emojis, name="usernamereg")} `a!usernamereg [java|bedrock] [username]`
<:space:846393726586191923> Register your Minecraft username.

{get(emojis, name="usernamequery")} `a!username [java|bedrock] [mentionuser]`
<:space:846393726586191923> Query a Minecraft username of a Discord user.""", color=0x36393f)

    embed2=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="leaderboard")} `a!bumpleader`
<:space:846393726586191923> Gives a leaderboard of bumps.

{get(emojis, name="leaderboard")} `a!invleader`
<:space:846393726586191923> Gives a leaderboard of invites.

{get(emojis, name="bump")} `!d bump`
<:space:846393726586191923> Bumps the server on DISBOARD.""", color=0x36393f)

    embed3=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="imgur")} `a!imgur`
<:space:846393726586191923> Attach images and the bot will upload them to Imgur.

{get(emojis, name="source")} `a!source`
<:space:846393726586191923> Returns the source code of the bot.

{get(emojis, name="avatar")} `a!da`
<:space:846393726586191923> Returns the color of a user's default avatar.

{get(emojis, name="dice")} `a!dice {{sides}} {{quantity}}`
<:space:846393726586191923> Rolls a number of fair dice with a number of sides each.

{get(emojis, name="coin")} `a!coin {{bet}}`
<:space:846393726586191923> Flip a coin; bet for heads or tails. Something might also happen...

{get(emojis, name="card")} `a!rank {{mentionuser}}`
<:space:846393726586191923> Returns a rank card of yours, or a specified user.""", color=0x36393f)

    embed4=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="faq")} `a!faq {{entry}}`
<:space:846393726586191923> Returns a list of frequently asked questions.

{get(emojis, name="lightmode")} `a!updateRankTheme [dark|light]`
<:space:846393726586191923> Changes the theme of rank cards for you.

{get(emojis, name="leaderboard")} `a!levels`
<:space:846393726586191923> Returns a leaderboard of levels.

{get(emojis, name="help")} `a!help`
<:space:846393726586191923> This command.""", color=0x36393f)
    embed1.set_footer(text="[] Required {} Optional")
    embed2.set_footer(text="[] Required {} Optional")
    embed3.set_footer(text="[] Required {} Optional")
    embed4.set_footer(text="[] Required {} Optional")
    embeds = [embed1, embed2, embed3, embed4]
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@bot.command()
async def send(ctx, *, content):
    """Send message in the user's command"""
    if ctx.author.id != 438298127225847810:
        await sendNoPermission(ctx=ctx)
        return
    await ctx.send(content)

#==================================================================    
=======
    emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
    from cogs.aesthetics import get_design, get_embedColor, get_icons

    title = f"{get(emojis, name='source')} " if get_icons()[str(ctx.author.id)] else ""
    title += "Source Code"
    embed = discord.Embed(
        title=title,
        description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot",
        color=int(get_embedColor()[str(ctx.author.id)], 16),
    )
    await ctx.send(embed=embed)


>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
### SLASH COMMANDS ZONE ###
#==================================================================  

from discord_slash import SlashCommand

slash = SlashCommand(bot, sync_commands=True, override_type=True)

guildID = 793495102566957096


@slash.slash(name="ping", description="Returns the latency in ms", guild_ids=[guildID])
async def _ping(ctx):
<<<<<<< HEAD
    """Returns the ping of the user"""
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
    await ctx.send(embed=embed)
    
@slash.slash(name="help",
             description="Returns the user guide of this bot",
             guild_ids=[guildID])
async def _help(ctx):
    """Shows menu UI"""
    # Format: {emoji} `full command` \n <space emoji> help text
    # TODO: Fix the UI
    emojis = bot.get_guild(846318304289488906).emojis
    embed1=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="ping")} `/ping`
<:space:846393726586191923> Returns the latency in ms.

{get(emojis, name="menu")} `/menu`
<:space:846393726586191923> Open the Navigation Menu.

{get(emojis, name="usernamereg")} `/usernamereg [java|bedrock] [username]`
<:space:846393726586191923> Register your Minecraft username.

{get(emojis, name="usernamequery")} `/username [java|bedrock] [mentionuser]`
<:space:846393726586191923> Query a Minecraft username of a Discord user.""", color=0x36393f)

    embed2=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="leaderboard")} `/bumpleader`
<:space:846393726586191923> Gives a leaderboard of bumps.

{get(emojis, name="leaderboard")} `/invleader`
<:space:846393726586191923> Gives a leaderboard of invites.

{get(emojis, name="source")} `/source`
<:space:846393726586191923> Returns the source code of the bot.

{get(emojis, name="avatar")} `/da`
<:space:846393726586191923> Returns the color of a user's default avatar.

{get(emojis, name="dice")} `/dice {{sides}} {{quantity}}`
<:space:846393726586191923> Rolls a number of fair dice with a number of sides each.

{get(emojis, name="coin")} `/coin {{bet}}`
<:space:846393726586191923> Flip a coin; bet for heads or tails. Something might also happen...""", color=0x36393f)

    embed3=discord.Embed(title=f"{get(emojis, name='help')} Aurum Bot User Guide", description=f"""{get(emojis, name="faq")} `/faq {{entry}}`
<:space:846393726586191923> Returns a list of frequently asked questions.
=======
    emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
    from cogs.aesthetics import get_design, get_embedColor, get_icons

    title = f"{get(emojis, name='ping')} " if get_icons()[str(ctx.author.id)] else ""
    title += "Ping"
    embed = discord.Embed(
        title=title,
        description=f"**{round(bot.latency * 1000)}ms**",
        color=int(get_embedColor()[str(ctx.author.id)], 16),
    )
    if not get_design()[str(ctx.author.id)]:
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_footer(text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png")
    await ctx.send(embed=embed)
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c


@slash.slash(
    name="source", description="Returns the source code of the bot", guild_ids=[guildID]
)
async def _source(ctx):
    """Shows message with source code github page"""
<<<<<<< HEAD
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='source')} Source Code", description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot", color=0x36393f)
=======
    emojis = bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
    from cogs.aesthetics import get_design, get_embedColor, get_icons

    title = f"{get(emojis, name='source')} " if get_icons()[str(ctx.author.id)] else ""
    title += "Source Code"
    embed = discord.Embed(
        title=title,
        description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot",
        color=int(get_embedColor()[str(ctx.author.id)], 16),
    )
>>>>>>> 4c0a95afa29edf0dd937b7e51b5c89b71e699b5c
    await ctx.send(embed=embed)


def run_bot():
    for i in [
        "design.json",
        "embedColor.json",
        "icons.json",
        "usernames.json",
        "xps.json",
    ]:
        f = open(i, "w")
        f.write("{}")
        f.close()
    for i in os.listdir("./cogs"):
        if i.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{i[:-3]}")
            except discord.ext.commands.errors.ExtensionNotFound:
                pass
    print("Extensions loaded!")
    bot.run(config("TOKEN"))


run_bot()

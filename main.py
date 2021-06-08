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
import requests

global prefix
prefix = 'a!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

token = config("TOKEN")
owner = config("OWNER")
botid = config("ID")

global botdev
botdev = str(owner)

async def sendNoPermission(ctx: Union[discord.ext.commands.Context, discord_slash.SlashContext, discord.TextChannel, discord.DMChannel, discord.GroupChannel]):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='error')} Error: No Permission", description="Sorry, but you don't have permission to do that.", color=0x36393f)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="try my slash commands!"))
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))
    global aliases
    aliases = []
    for command in bot.commands:
        aliases += (list(command.aliases) + [command.name])

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(793513021288742912)
    if member.guild.id != 793495102566957096:
        return
    await channel.send("<:oslash:803836347097677844>")
    await channel.send(f"<@{member.id}> has joined the server. Welcome, <@{member.id}>.\nRefer to <#793529403233665084> for rules and <#793513974582607962> for joining instructions.\nUse <#793626862180892732> to assign some roles for yourself.\nNeed help? Use `/faq`!")

@bot.event
async def on_member_remove(member):
    if member.guild.id != 793495102566957096:
        return
    channel = bot.get_channel(793513021288742912)
    await channel.send(f"**{member.name}#{member.discriminator}** has left the server. Farewell, **{member.name}#{member.discriminator}**.")
    
## Message edit detection
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)
    
@bot.event
async def on_command_error(ctx, error):
    triedCommand = ctx.message.content.split(" ")[0][2:]
    a = 1
    # If user added a space between prefix and command
    while len(triedCommand) == 0:
        triedCommand = ctx.message.content.split(" ")[a]
        a += 1
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        try:
            closest = difflib.get_close_matches(triedCommand, aliases)[0]
            emojis = bot.get_guild(846318304289488906).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Command", description=f"Use `a!help` if you need help.\nDid you mean `a!{closest}`?", color=0x36393f)
            await ctx.send(embed=embed)
        except IndexError:
            emojis = bot.get_guild(846318304289488906).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Command", description=f"Use `a!help` if you need help.", color=0x36393f)
            await ctx.send(embed=embed)

@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        await sendNoPermission(ctx=ctx)

@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        await sendNoPermission(ctx=ctx)

@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
    else:
        await sendNoPermission(ctx=ctx)

@bot.command()
async def extlist(ctx):
    if str(ctx.author.id) == str(owner):
        exts = []
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                exts.append(i[:-3])
        message1 = ''
        for j in exts:
            message1 += f'''`{j}`\n'''
        await ctx.send(message1)
    else:
        await sendNoPermission(ctx=ctx)
    
@bot.command(name='exec')
async def exec_command(ctx, *, arg1):
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
    if str(ctx.author.id) != botdev:
        await sendNoPermission(ctx=ctx)
        return
    for i in os.listdir("./cogs"):
        if i.endswith(".py"):
            try:
                bot.load_extension(f'cogs.{i[:-3]}')
                await ctx.send(f"Loaded {i[:-3]}")
            except discord.ext.commands.errors.ExtensionNotFound:
                await ctx.send(f"Can't load {i[:-3]}")
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                await ctx.send(f"Already loaded {i[:-3]}")
                
@tasks.loop(minutes=1)
async def denyDankAccess():
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
    embed = discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
    await ctx.send(embed=embed)

@bot.command()
async def source(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='source')} Source Code", description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot", color=0x36393f)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
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
    if ctx.author.id != 438298127225847810:
        await sendNoPermission(ctx=ctx)
        return
    await ctx.send(content)
    
### SLASH COMMANDS ZONE ###

from discord_slash import SlashCommand
slash = SlashCommand(bot, sync_commands=True, override_type=True)

guildID = 793495102566957096

@slash.slash(name="ping", 
             description="Returns the latency in ms",
             guild_ids=[guildID])
async def _ping(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
    await ctx.send(embed=embed)
    
@slash.slash(name="help",
             description="Returns the user guide of this bot",
             guild_ids=[guildID])
async def _help(ctx):
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

{get(emojis, name="card")} `/rank {{mentionuser}}`
<:space:846393726586191923> Returns a rank card of yours, or a specified user.

{get(emojis, name="lightmode")} `/updateRankTheme [dark|light]`
<:space:846393726586191923> Changes the theme of rank cards for you.

{get(emojis, name="leaderboard")} `/levels`
<:space:846393726586191923> Returns a leaderboard of levels.

{get(emojis, name="help")} `/help`
<:space:846393726586191923> This command.""", color=0x36393f)
    embed1.set_footer(text="[] Required {} Optional")
    embed2.set_footer(text="[] Required {} Optional")
    embed3.set_footer(text="[] Required {} Optional")
    embeds = [embed1, embed2, embed3]
    paginator = BotEmbedPaginator(ctx, embeds)
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='error')} Refer below!", description="Refer to the message below for the help menu.", color=0x36393f)
    await ctx.send(embed=embed)
    await paginator.run()
    
@slash.slash(name="source",
             description="Returns the source code of the bot",
             guild_ids=[guildID])
async def _source(ctx):
    emojis = bot.get_guild(846318304289488906).emojis
    embed = discord.Embed(title=f"{get(emojis, name='source')} Source Code", description="Here is the source code of the bot:\nhttps://github.com/Aurum-Minecraft-Network/Aurum-Bot", color=0x36393f)
    await ctx.send(embed=embed)
    
def runBot():    
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{i[:-3]}')
            except discord.ext.commands.errors.ExtensionNotFound:
                pass
    print('Extensions loaded!')
    bot.run(token)
    
runBot()
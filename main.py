import discord
import os
import sys
import io
import traceback
import yaml
from decouple import config
from discord.ext import commands
import difflib

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

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="try my slash commands!"))
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))
    global aliases
    aliases = []
    for command in bot.commands:
        aliases += (list(command.aliases) + [command.name])

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(793513021288742912)
    await channel.send("<:oslash:803836347097677844>")
    await channel.send(f"<@{member.id}> has joined the server. Welcome, <@{member.id}>.\nRefer to <#793529403233665084> for rules and <#793513974582607962> for joining instructions.\nUse <#793626862180892732> to assign some roles for yourself.\nNeed help? Use `/faq`!")

@bot.event
async def on_member_remove(member):
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
            await ctx.channel.send(f"Invalid command! Did you mean `a!{closest}`?")
        except IndexError:
            await ctx.channel.send("Invalid command!")

@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

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
        await ctx.send("Sorry, but you don't have permission to do that.")
    
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
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

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
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Input", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Definition Success!', color=0x00ff00)
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Function Definition", value=f'```py\n{str(func)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

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
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**.')

@bot.command()
async def source(ctx):
    await ctx.send(f"Here is the source code of the bot:\nhttps://github.com/ATP-City/ATP-City-Bot")

@bot.command()
async def help(ctx):
    await ctx.send("""***ATP City Bot User Guide***
`a!ping`
Returns the latency in ms.

`a!help`
This command.

`a!usernamereg [java|bedrock] [username]`
Register your Minecraft username.

`a!username [java|bedrock] [mentionuser]`
Query a Minecraft username of a Discord user.

`a!bumpleader`
Gives a leaderboard of bumps.

`a!invleader`
Gives a leaderboard of invites.

`!d bump`
Bumps the server on DISBOARD.

`a!imgur`
Attach images and the bot will upload them to Imgur.

`a!source`
Returns the source code of the bot.

`a!da`
Returns the color of a user's default avatar.

`a!faq`
Returns a list of frequently asked questions.

`a!rank`
Returns a rank card of yours, or a specified user.

`a!updateranktheme`
Changes the theme of rank cards for you.

`a!levels`
Returns a leaderboard of levels.""")

@bot.command(aliases=["cs"])
async def competitionsubmit(ctx, *, submission):
    with open("nc.yaml") as f:
        entries = yaml.full_load(f)
    entries.update({f"{ctx.author.id}": f"{submission}"})
    with open("nc.yaml", "w") as f:
        yaml.dump(entries, f)
    await ctx.send(f"Submitted your entry:\n{submission}")

@bot.command()
async def send(ctx, *, content):
    if ctx.author.id != 438298127225847810:
        await ctx.send("Sorry, but you do not have permission to do that.")
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
    await ctx.send(f':ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**.')
    
@slash.slash(name="help",
             description="Returns the user guide of this bot",
             guild_ids=[guildID])
async def _help(ctx):
    await ctx.send("""***ATP City Bot User Guide***
`/ping`
Returns the latency in ms.

`/help`
This command.

`/usernamereg [java|bedrock] [username]`
Register your Minecraft username.

`/username [java|bedrock] [mentionuser]`
Query a Minecraft username of a Discord user.

`/bumpleader`
Gives a leaderboard of bumps.

`/invleader`
Gives a leaderboard of invites.

`/source`
Returns the source code of the bot.

`/da`
Returns the color of a user's default avatar.

`/faq`
Returns a list of frequently asked questions.

`/rank`
Returns a rank card of yours, or a specified user.

`/updateranktheme`
Changes the theme of rank cards for you.

`/levels`
Returns a leaderboard of levels.""")
    
@slash.slash(name="source",
             description="Returns the source code of the bot",
             guild_ids=[guildID])
async def _source(ctx):
    await ctx.send(f"Here is the source code of the bot:\nhttps://github.com/ATP-City/ATP-City-Bot")
    
def runBot():    
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            bot.load_extension(f'cogs.{i[:-3]}')
    print('Extensions loaded!')
    bot.run(token)
    
runBot()
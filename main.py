import discord
import os
import sys
import io
import traceback
from decouple import config
from discord.ext import commands

global prefix
prefix = 'a!'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

token = config("TOKEN")
owner = config("OWNER")
botid = config("ID")

global botdev
botdev = str(owner)

@bot.event
async def on_ready():
    global bumpDone
    bumpDone = False
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))

for i in os.listdir('./cogs'):
    if i.endswith('.py'):
        bot.load_extension(f'cogs.{i[:-3]}')
print('Extensions loaded!')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(793513021288742912)
    await channel.send(f"<@{member.id}> has joined the server. Welcome, <@{member.id}>\nRefer to <#793529403233665084> for rules and <#793513974582607962> for joining instructions.")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(793513021288742912)
    await channel.send(f"**{member.name}#{member.discriminator}** has left the server. Farewell, **{member.name}#{member.discriminator}**.")

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
            await ctx.send(embed = embed)
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

`a!source`
Returns the source code of the bot.""")

bot.run(token)
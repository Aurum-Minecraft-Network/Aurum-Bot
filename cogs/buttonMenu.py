import discord
from discord.ext import commands
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from PIL import Image, ImageDraw, ImageFont
import json
from collections import OrderedDict, defaultdict
from decouple import config
import boto3
import pyimgur
import os

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

## Imgur setup
imgurid = config("IMGURID")
imgur = pyimgur.Imgur(imgurid)

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def getDark(self):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864231847559198)
        return json.loads(msg.content)
    
    async def updateDark(self, dict):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864231847559198)
        await msg.edit(content=json.dumps(dict, indent=4))
        
    def getLevelXP(self, level: int):
        return 5 * ((level-1) ** 2) + (50 * (level-1)) + 100 if level > 1 else 100

    def getLevelTotalXP(self, level: int):
        xp = 0
        while level > 0:
            xp += self.getLevelXP(level)
            level -= 1
        return xp

    def getLevelFromTotalXP(self, xp: int):
        n = 1
        a = self.getLevelTotalXP(n)
        while a < xp:
            n += 1
            a = self.getLevelTotalXP(n)
        return n-1 if a > xp else n
        
    async def getXP(self):
        return defaultdict(int, OrderedDict(reversed(list({k: v for k, v in sorted(json.loads(client.get_object(Bucket="atpcitybot", Key="xps.json")["Body"].read()).items(), key=lambda item: item[1])}.items()))))
    
    async def updateXP(self, dictionary):
        dictionary = OrderedDict(reversed(list({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}.items())))
        with open("xps.json", "w") as f:
            json.dump(dictionary, f, indent=4)
        with open("xps.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "xps.json")
        
    async def getBumps(self): # Get bump JSON string from channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798226999238983750)
        return json.loads(msg.content)

    async def getInvs(self): # Get JSON string of number of users each user invited in Discord channel
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(798227110892273684)
        return json.loads(msg.content)

    @commands.command()
    async def menu(self, ctx):
        emojis = self.bot.get_guild(846318304289488906).emojis

        if ctx.message.author.bot:
            return

        curr = "topMenu"

        topMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='menu')} Aurum Bot Navigation Menu", description="Choose an option to proceed.", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.blue, label="Ping", emoji=get(emojis, name='ping')),
                    Button(style=ButtonStyle.blue, label="Levelling", emoji=get(emojis, name='lvup')),
                    Button(style=ButtonStyle.blue, label="Leaderboards", emoji=get(emojis, name='leaderboard'))
                ],
                [
                    Button(style=ButtonStyle.URL, label="Source Code", url="https://github.com/Aurum-Minecraft-Network/Aurum-Bot", emoji=get(emojis, name='source')),
                    Button(style=ButtonStyle.URL, label="Aurum Minecraft Network Discord Server", emoji=get(emojis, name='aurum'), url="https://discord.aurummcnet.ga")
                ]
            ],
        }

        pingMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(self.bot.latency * 1000)}ms**", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        levelMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='lvup')} Aurum Bot Levelling Menu", description="Choose an option to proceed.", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.blue, label="Get Own Rank Card", emoji=get(emojis, name='card')),
                    Button(style=ButtonStyle.blue, label="Change Rank Card Theme", emoji=get(emojis, name='lightmode'))
                ],
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        changeRankThemeMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='card')} Change Rank Card Theme", description="Choose an option to proceed.", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.blue, label="Light Theme", emoji=get(emojis, name='lightmode')),
                    Button(style=ButtonStyle.blue, label="Dark Theme", emoji=get(emojis, name='darkmode'))
                ],
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        changeRankThemeLightMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='success')} Update Successful", description=f"{get(emojis, name='lightmode')} Your theme has been updated to the light theme!", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        changeRankThemeDarkMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='success')} Update Successful", description=f"{get(emojis, name='darkmode')} Your theme has been updated to the dark theme!", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        leaderMenu = {
            "embed": discord.Embed(title=f"{get(emojis, name='leaderboard')} Aurum Bot Leaderboard Menu", description="Choose an option to proceed.", color=0x36393f),
            "components": [
                [
                    Button(style=ButtonStyle.blue, label="XP Leaderboard", emoji=get(emojis, name='lvup')),
                    Button(style=ButtonStyle.blue, label="Bump Leaderboard", emoji=get(emojis, name='bump')),
                    Button(style=ButtonStyle.blue, label="Invite Leaderboard", emoji=get(emojis, name='usernamereg'))
                ],
                [
                    Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                ]
            ],
        }

        await ctx.message.channel.send(**topMenu)

        while True:
            res = await self.bot.wait_for("button_click")
            if res.channel == ctx.message.channel:
                ## topMenu
                if curr == "topMenu" and res.component.label == "Ping":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **pingMenu
                    )
                    curr = "pingMenu"
                elif curr == "topMenu" and res.component.label == "Levelling":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **levelMenu
                    )
                    curr = "levelMenu"
                elif curr == "topMenu" and res.component.label == "Leaderboards":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **leaderMenu
                    )
                    curr = "leaderMenu"
                    
                ## pingMenu
                elif curr == "pingMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **topMenu
                    )
                    curr = "topMenu"
                    
                ## levelMenu
                elif curr == "levelMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **topMenu
                    )
                    curr = "topMenu"
                elif curr == "levelMenu" and res.component.label == "Change Rank Card Theme":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **changeRankThemeMenu
                    )
                    curr = "changeRankThemeMenu"
                elif curr == "levelMenu" and res.component.label == "Get Own Rank Card":
                    embed = discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description="This may take a while...", color=0x36393f)
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        embed=embed,
                        components=[]
                    )
                    curr = "rankCardMenu"
                    user = ctx.message.author
                    try:
                        dark = (await self.getDark())[str(ctx.message.author.id)]
                    except KeyError:
                        darks = await self.getDark()
                        darks.update({str(ctx.message.author.id): True})
                        await self.updateDark(darks)
                        dark = True
                    print(user)
                    if dark:
                        textColor = "white"
                        bgColor = "#36393f"
                        barColor = "white"
                    else:
                        textColor = "black"
                        bgColor = "#ffffff"
                        barColor = "black"
                    ## Fonts
                    rodinpro50 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 50)
                    rodinpro80 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 80)
                    whitney65 = ImageFont.truetype("assets/fonts/whitney.ttf", 65)
                    ## Download avatar
                    await user.avatar_url.save("avatar.png")
                    avatar = Image.open("avatar.png", "r").resize((140, 140))
                    ## Background
                    xps = await self.getXP()
                    level = self.getLevelFromTotalXP(xps[str(user.id)])
                    im = Image.new("RGBA", (1000, 460), bgColor)
                    im.paste(avatar, (30, 30))
                    os.remove("avatar.png")
                    try:
                        rank = list(xps.keys()).index(str(user.id)) + 1
                    except KeyError:
                        rank = list(xps.keys())
                        rank.append(str(user.id))
                        rank = len(rank)
                    d = ImageDraw.Draw(im)
                    d.text((195, 100), f"{user.name}#{user.discriminator}", fill=textColor, anchor="lm", font=whitney65)
                    d.text((30, 430), "Rank", fill=textColor, anchor="lb", font=rodinpro50)
                    d.text((170, 430), "#" + str(rank), fill=textColor, anchor="lb", font=rodinpro80)
                    d.text((30, 280), "Level", fill=textColor, anchor="lb", font=rodinpro50)
                    d.text((180, 280), str(level), fill=textColor, anchor="lb", font=rodinpro80)
                    
                    def round_corner(radius, fill):
                        """Draw a round corner"""
                        corner = Image.new('RGB', (radius, radius), bgColor)
                        draw = ImageDraw.Draw(corner)
                        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
                        return corner

                    def round_rectangle(size, radius, fill, x):
                        """Draw a rounded rectangle"""
                        width, height = size
                        rectangle = Image.new('RGBA', size, fill)
                        corner = round_corner(radius, fill)
                        rectangle.paste(corner, (0, 0))
                        rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
                        if x:
                            rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                            rectangle.paste(corner.rotate(270), (width - radius, 0))
                        return rectangle
                    
                    xp = xps[str(user.id)] - self.getLevelTotalXP(level) # Current level XP
                    targetxp = self.getLevelXP(level+1)
                    
                    im.paste(round_rectangle((940, 50), 25, barColor, True), (30, 300))
                    im.paste(round_rectangle((round(940 * (xp / targetxp)), 50), 25, "blue", False), (30, 300))
                    
                    d.text((970, 280), f"{xp} / {targetxp} XP", fill=textColor, anchor="rb", font=rodinpro50)
                    im.save("rank.png")
                    embed = discord.Embed(title=f"{get(emojis, name='card')} Rank Card", color=0x36393f)
                    uploaded_image = imgur.upload_image(os.path.abspath("./rank.png"), title="Aurum Bot Rank Card")
                    print(uploaded_image.link)
                    embed.set_image(url=uploaded_image.link)
                    os.remove("rank.png")
                    await res.message.edit(
                        type=InteractionType.ChannelMessageWithSource,
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                            ]
                        ]
                    )
                    
                ## rankCardMenu
                elif curr == "rankCardMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **levelMenu
                    )
                    curr = "levelMenu"
                    
                ## changeRankThemeMenu
                elif curr == "changeRankThemeMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **levelMenu
                    )
                    curr = "levelMenu"
                elif curr == "changeRankThemeMenu" and res.component.label == "Light Theme":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **changeRankThemeLightMenu
                    )
                    curr = "changeRankThemeLightMenu"
                    darks = await self.getDark()
                    darks.update({str(ctx.message.author.id): False})
                    await self.updateDark(darks)
                elif curr == "changeRankThemeMenu" and res.component.label == "Dark Theme":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **changeRankThemeDarkMenu
                    )
                    curr = "changeRankThemeDarkMenu"
                    darks = await self.getDark()
                    darks.update({str(ctx.message.author.id): True})
                    await self.updateDark(darks)
                    
                ## changeRankThemeLightMenu
                elif curr == "changeRankThemeLightMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **changeRankThemeMenu
                    )
                    curr = "changeRankThemeMenu"
                    
                ## changeRankThemeDarkMenu
                elif curr == "changeRankThemeDarkMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **changeRankThemeMenu
                    )
                    curr = "changeRankThemeMenu"
                    
                ## leaderMenu
                elif curr == "leaderMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **topMenu
                    )
                    curr = "topMenu"
                elif curr == "leaderMenu" and res.component.label == "XP Leaderboard":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        embed=discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description="This may take a while...", color=0x36393f),
                        components=[]
                    )
                    curr = "xpLeaderMenu"
                    msg = ""
                    rank = 1
                    xps = await self.getXP()
                    newXPS = []
                    for key, value in zip(list(xps.keys()), list(xps.values())):
                        newXPS.append([key, value])
                    xps = newXPS
                    del newXPS
                    guild = self.bot.get_guild(793495102566957096)
                    for pair in xps:
                        print(pair, "pair")
                        user = guild.get_member(int(pair[0]))
                        print(user)
                        if not user:
                            xps.remove(pair)
                            await self.updateXP(OrderedDict(xps))
                            continue
                        msg += "{}. {}#{}\n".format(rank, user.name, user.discriminator)
                        rank += 1
                        await res.message.edit(
                            type=InteractionType.ChannelMessageWithSource,
                            embed=discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description=f"This may take a while...\n**{rank-1}/{len(xps)}**", color=0x36393f),
                            components=[]
                        )
                    embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} XP Leaderboard", description=msg, color=0x36393f)
                    await res.message.edit(
                        type=InteractionType.ChannelMessageWithSource,
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                            ]
                        ]
                    )
                elif curr == "leaderMenu" and res.component.label == "Bump Leaderboard":
                    bumpss = await self.getBumps() # Get bump data of all users
                    bumps = bumpss
                    del bumps["lastBump"]
                    leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True)) # Sort the dictionary from user with most bumps to least bumps
                    leaderv = list(leaders.values()) # Number of bumps
                    leaderk = list(leaders.keys()) # User ID
                    msg = ""
                    rank = int(leaderv[0]) # Highest number of bumps
                    place = 1
                    usersDone = 0
                    for name, bumpe in zip(leaderk, leaderv):
                        guild = self.bot.get_guild(793495102566957096)
                        for users in guild.members:
                            if str(users.id) == str(name):
                                user = users # Found the user in the guild which the user ID represents
                            else:
                                continue
                            if rank > int(bumpe): # This user has less bumps than the previous user
                                place += 1 # So he/ she is one place lower
                                rank = int(leaderv[usersDone]) # Set rank to the number of bumps done by this user
                            ## else: pass
                            ## Same no. of bumps as the previous user, same place!
                            msg += f"\n**{str(place)}.** {user.name}#{user.discriminator} - __{rank}__ Bump"
                            ## Should we make the word "Bump" plural?
                            if rank > 1:
                                msg += "s"
                            usersDone += 1
                    embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Bump Leaderboard", description=msg, color=0x36393f)
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                            ]
                        ]
                    )
                    curr = "bumpLeaderMenu"
                    
                elif curr == "leaderMenu" and res.component.label == "Invite Leaderboard":
                    bumps = await self.getInvs()
                    leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
                    leaderv = list(leaders.values())
                    leaderk = list(leaders.keys())
                    msg = ""
                    rank = int(leaderv[0])
                    place = 1
                    usersDone = 0
                    for name, bumpe in zip(leaderk, leaderv):
                        guild = self.bot.get_guild(793495102566957096)
                        for users in guild.members:
                            if str(users.id) == str(name):
                                user = users
                            else:
                                continue
                            if rank > int(bumpe):
                                place += 1
                                rank = int(leaderv[usersDone])
                            msg += f"\n**{str(place)}.** {user.name}#{user.discriminator} - __{rank}__ Invite"
                            if rank > 1:
                                msg += "s"
                            usersDone += 1
                    emojis = self.bot.get_guild(846318304289488906).emojis
                    embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Invite Leaderboard", description=msg, color=0x36393f)
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                            ]
                        ]
                    )
                    curr = "invLeaderMenu"
                    
                ## xpLeaderMenu
                elif curr == "xpLeaderMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **leaderMenu
                    )
                    curr = "leaderMenu"
                    
                ## bumpLeaderMenu
                elif curr == "bumpLeaderMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **leaderMenu
                    )
                    curr = "leaderMenu"
                    
                ## invLeaderMenu
                elif curr == "invLeaderMenu" and res.component.label == "Go Back":
                    await res.respond(
                        type=InteractionType.UpdateMessage,
                        **leaderMenu
                    )
                    curr = "leaderMenu"
                    
### SLASH COMMANDS ZONE ###

guildID = 793495102566957096

@cog_ext.cog_slash(name="menu", 
             description="Open the Navigation Menu",
             guild_ids=[guildID])
async def _menu(self, ctx: SlashContext):
    emojis = self.bot.get_guild(846318304289488906).emojis
    
    if ctx.message.author.bot:
        return

    curr = "topMenu"
    
    topMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='menu')} Aurum Bot Navigation Menu", description="Choose an option to proceed.", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.blue, label="Ping", emoji=get(emojis, name='ping')),
                Button(style=ButtonStyle.blue, label="Levelling", emoji=get(emojis, name='lvup')),
                Button(style=ButtonStyle.blue, label="Leaderboards", emoji=get(emojis, name='leaderboard'))
            ],
            [
                Button(style=ButtonStyle.URL, label="Source Code", url="https://github.com/Aurum-Minecraft-Network/Aurum-Bot", emoji=get(emojis, name='source')),
                Button(style=ButtonStyle.URL, label="Aurum Minecraft Network Discord Server", emoji=get(emojis, name='aurum'), url="https://discord.aurummcnet.ga")
            ]
        ],
    }
    
    pingMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='ping')} Ping", description=f"**{round(self.bot.latency * 1000)}ms**", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }
    
    levelMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='lvup')} Aurum Bot Levelling Menu", description="Choose an option to proceed.", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.blue, label="Get Own Rank Card", emoji=get(emojis, name='card')),
                Button(style=ButtonStyle.blue, label="Change Rank Card Theme", emoji=get(emojis, name='lightmode'))
            ],
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }
    
    changeRankThemeMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='card')} Change Rank Card Theme", description="Choose an option to proceed.", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.blue, label="Light Theme", emoji=get(emojis, name='lightmode')),
                Button(style=ButtonStyle.blue, label="Dark Theme", emoji=get(emojis, name='darkmode'))
            ],
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }
    
    changeRankThemeLightMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='success')} Update Successful", description=f"{get(emojis, name='lightmode')} Your theme has been updated to the light theme!", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }
    
    changeRankThemeDarkMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='success')} Update Successful", description=f"{get(emojis, name='darkmode')} Your theme has been updated to the dark theme!", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }
    
    leaderMenu = {
        "embed": discord.Embed(title=f"{get(emojis, name='leaderboard')} Aurum Bot Leaderboard Menu", description="Choose an option to proceed.", color=0x36393f),
        "components": [
            [
                Button(style=ButtonStyle.blue, label="XP Leaderboard", emoji=get(emojis, name='lvup')),
                Button(style=ButtonStyle.blue, label="Bump Leaderboard", emoji=get(emojis, name='bump')),
                Button(style=ButtonStyle.blue, label="Invite Leaderboard", emoji=get(emojis, name='usernamereg'))
            ],
            [
                Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
            ]
        ],
    }

    await ctx.message.channel.send(**topMenu)

    while True:
        res = await self.bot.wait_for("button_click")
        if res.channel == ctx.message.channel:
            ## topMenu
            if curr == "topMenu" and res.component.label == "Ping":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **pingMenu
                )
                curr = "pingMenu"
            elif curr == "topMenu" and res.component.label == "Levelling":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **levelMenu
                )
                curr = "levelMenu"
            elif curr == "topMenu" and res.component.label == "Leaderboards":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **leaderMenu
                )
                curr = "leaderMenu"
                
            ## pingMenu
            elif curr == "pingMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **topMenu
                )
                curr = "topMenu"
                
            ## levelMenu
            elif curr == "levelMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **topMenu
                )
                curr = "topMenu"
            elif curr == "levelMenu" and res.component.label == "Change Rank Card Theme":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **changeRankThemeMenu
                )
                curr = "changeRankThemeMenu"
            elif curr == "levelMenu" and res.component.label == "Get Own Rank Card":
                embed = discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description="This may take a while...", color=0x36393f)
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    embed=embed,
                    components=[]
                )
                curr = "rankCardMenu"
                user = ctx.message.author
                try:
                    dark = (await self.getDark())[str(ctx.message.author.id)]
                except KeyError:
                    darks = await self.getDark()
                    darks.update({str(ctx.message.author.id): True})
                    await self.updateDark(darks)
                    dark = True
                print(user)
                if dark:
                    textColor = "white"
                    bgColor = "#36393f"
                    barColor = "white"
                else:
                    textColor = "black"
                    bgColor = "#ffffff"
                    barColor = "black"
                ## Fonts
                rodinpro50 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 50)
                rodinpro80 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 80)
                whitney65 = ImageFont.truetype("assets/fonts/whitney.ttf", 65)
                ## Download avatar
                await user.avatar_url.save("avatar.png")
                avatar = Image.open("avatar.png", "r").resize((140, 140))
                ## Background
                xps = await self.getXP()
                level = self.getLevelFromTotalXP(xps[str(user.id)])
                im = Image.new("RGBA", (1000, 460), bgColor)
                im.paste(avatar, (30, 30))
                os.remove("avatar.png")
                try:
                    rank = list(xps.keys()).index(str(user.id)) + 1
                except KeyError:
                    rank = list(xps.keys())
                    rank.append(str(user.id))
                    rank = len(rank)
                d = ImageDraw.Draw(im)
                d.text((195, 100), f"{user.name}#{user.discriminator}", fill=textColor, anchor="lm", font=whitney65)
                d.text((30, 430), "Rank", fill=textColor, anchor="lb", font=rodinpro50)
                d.text((170, 430), "#" + str(rank), fill=textColor, anchor="lb", font=rodinpro80)
                d.text((30, 280), "Level", fill=textColor, anchor="lb", font=rodinpro50)
                d.text((180, 280), str(level), fill=textColor, anchor="lb", font=rodinpro80)
                
                def round_corner(radius, fill):
                    """Draw a round corner"""
                    corner = Image.new('RGB', (radius, radius), bgColor)
                    draw = ImageDraw.Draw(corner)
                    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
                    return corner

                def round_rectangle(size, radius, fill, x):
                    """Draw a rounded rectangle"""
                    width, height = size
                    rectangle = Image.new('RGBA', size, fill)
                    corner = round_corner(radius, fill)
                    rectangle.paste(corner, (0, 0))
                    rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
                    if x:
                        rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                        rectangle.paste(corner.rotate(270), (width - radius, 0))
                    return rectangle
                
                xp = xps[str(user.id)] - self.getLevelTotalXP(level) # Current level XP
                targetxp = self.getLevelXP(level+1)
                
                im.paste(round_rectangle((940, 50), 25, barColor, True), (30, 300))
                im.paste(round_rectangle((round(940 * (xp / targetxp)), 50), 25, "blue", False), (30, 300))
                
                d.text((970, 280), f"{xp} / {targetxp} XP", fill=textColor, anchor="rb", font=rodinpro50)
                im.save("rank.png")
                embed = discord.Embed(title=f"{get(emojis, name='card')} Rank Card", color=0x36393f)
                uploaded_image = imgur.upload_image(os.path.abspath("./rank.png"), title="Aurum Bot Rank Card")
                print(uploaded_image.link)
                embed.set_image(url=uploaded_image.link)
                os.remove("rank.png")
                await res.message.edit(
                    type=InteractionType.ChannelMessageWithSource,
                    embed=embed,
                    components=[
                        [
                            Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                        ]
                    ]
                )
                
            ## rankCardMenu
            elif curr == "rankCardMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **levelMenu
                )
                curr = "levelMenu"
                
            ## changeRankThemeMenu
            elif curr == "changeRankThemeMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **levelMenu
                )
                curr = "levelMenu"
            elif curr == "changeRankThemeMenu" and res.component.label == "Light Theme":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **changeRankThemeLightMenu
                )
                curr = "changeRankThemeLightMenu"
                darks = await self.getDark()
                darks.update({str(ctx.message.author.id): False})
                await self.updateDark(darks)
            elif curr == "changeRankThemeMenu" and res.component.label == "Dark Theme":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **changeRankThemeDarkMenu
                )
                curr = "changeRankThemeDarkMenu"
                darks = await self.getDark()
                darks.update({str(ctx.message.author.id): True})
                await self.updateDark(darks)
                
            ## changeRankThemeLightMenu
            elif curr == "changeRankThemeLightMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **changeRankThemeMenu
                )
                curr = "changeRankThemeMenu"
                
            ## changeRankThemeDarkMenu
            elif curr == "changeRankThemeDarkMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **changeRankThemeMenu
                )
                curr = "changeRankThemeMenu"
                
            ## leaderMenu
            elif curr == "leaderMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **topMenu
                )
                curr = "topMenu"
            elif curr == "leaderMenu" and res.component.label == "XP Leaderboard":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    embed=discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description="This may take a while...", color=0x36393f),
                    components=[]
                )
                curr = "xpLeaderMenu"
                msg = ""
                rank = 1
                xps = await self.getXP()
                newXPS = []
                for key, value in zip(list(xps.keys()), list(xps.values())):
                    newXPS.append([key, value])
                xps = newXPS
                del newXPS
                guild = self.bot.get_guild(793495102566957096)
                for pair in xps:
                    print(pair, "pair")
                    user = guild.get_member(int(pair[0]))
                    print(user)
                    if not user:
                        xps.remove(pair)
                        await self.updateXP(OrderedDict(xps))
                        continue
                    msg += "{}. {}#{}\n".format(rank, user.name, user.discriminator)
                    rank += 1
                    await res.message.edit(
                        type=InteractionType.ChannelMessageWithSource,
                        embed=discord.Embed(title=f"{get(emojis, name='wait')} Please wait...", description=f"This may take a while...\n**{rank-1}/{len(xps)}**", color=0x36393f),
                        components=[]
                    )
                embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} XP Leaderboard", description=msg, color=0x36393f)
                await res.message.edit(
                    type=InteractionType.ChannelMessageWithSource,
                    embed=embed,
                    components=[
                        [
                            Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                        ]
                    ]
                )
            elif curr == "leaderMenu" and res.component.label == "Bump Leaderboard":
                bumpss = await self.getBumps() # Get bump data of all users
                bumps = bumpss
                del bumps["lastBump"]
                leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True)) # Sort the dictionary from user with most bumps to least bumps
                leaderv = list(leaders.values()) # Number of bumps
                leaderk = list(leaders.keys()) # User ID
                msg = ""
                rank = int(leaderv[0]) # Highest number of bumps
                place = 1
                usersDone = 0
                for name, bumpe in zip(leaderk, leaderv):
                    guild = self.bot.get_guild(793495102566957096)
                    for users in guild.members:
                        if str(users.id) == str(name):
                            user = users # Found the user in the guild which the user ID represents
                        else:
                            continue
                        if rank > int(bumpe): # This user has less bumps than the previous user
                            place += 1 # So he/ she is one place lower
                            rank = int(leaderv[usersDone]) # Set rank to the number of bumps done by this user
                        ## else: pass
                        ## Same no. of bumps as the previous user, same place!
                        msg += f"\n**{str(place)}.** {user.name}#{user.discriminator} - __{rank}__ Bump"
                        ## Should we make the word "Bump" plural?
                        if rank > 1:
                            msg += "s"
                        usersDone += 1
                embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Bump Leaderboard", description=msg, color=0x36393f)
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    embed=embed,
                    components=[
                        [
                            Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                        ]
                    ]
                )
                curr = "bumpLeaderMenu"
                
            elif curr == "leaderMenu" and res.component.label == "Invite Leaderboard":
                bumps = await self.getInvs()
                leaders = dict(sorted(bumps.items(), key=lambda x: x[1], reverse=True))
                leaderv = list(leaders.values())
                leaderk = list(leaders.keys())
                msg = ""
                rank = int(leaderv[0])
                place = 1
                usersDone = 0
                for name, bumpe in zip(leaderk, leaderv):
                    guild = self.bot.get_guild(793495102566957096)
                    for users in guild.members:
                        if str(users.id) == str(name):
                            user = users
                        else:
                            continue
                        if rank > int(bumpe):
                            place += 1
                            rank = int(leaderv[usersDone])
                        msg += f"\n**{str(place)}.** {user.name}#{user.discriminator} - __{rank}__ Invite"
                        if rank > 1:
                            msg += "s"
                        usersDone += 1
                emojis = self.bot.get_guild(846318304289488906).emojis
                embed = discord.Embed(title=f"{get(emojis, name='leaderboard')} Invite Leaderboard", description=msg, color=0x36393f)
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    embed=embed,
                    components=[
                        [
                            Button(style=ButtonStyle.grey, label="Go Back", emoji=get(emojis, name='back'))
                        ]
                    ]
                )
                curr = "invLeaderMenu"
                
            ## xpLeaderMenu
            elif curr == "xpLeaderMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **leaderMenu
                )
                curr = "leaderMenu"
                
            ## bumpLeaderMenu
            elif curr == "bumpLeaderMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **leaderMenu
                )
                curr = "leaderMenu"
                
            ## invLeaderMenu
            elif curr == "invLeaderMenu" and res.component.label == "Go Back":
                await res.respond(
                    type=InteractionType.UpdateMessage,
                    **leaderMenu
                )
                curr = "leaderMenu"

def setup(bot):
    bot.add_cog(Buttons(bot))

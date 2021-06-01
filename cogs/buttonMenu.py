import discord
from discord.ext import commands
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from PIL import Image, ImageDraw, ImageFont
import time
import os
from collections import OrderedDict

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
                        **topMenu
                    )
                    emojis = self.bot.get_guild(846318304289488906).emojis
                    try:
                        dark = (await self.getDark())[str(ctx.author.id)]
                    except KeyError:
                        darks = await self.getDark()
                        darks.update({str(ctx.author.id): True})
                        await self.updateDark(darks)
                        dark = True
                    if dark:
                        textColor = "white"
                        bgColor = "#36393f"
                    else:
                        textColor = "black"
                        bgColor = "#ffffff"
                    xps = await self.getXP()
                    newXPS = []
                    for key, value in zip(list(xps.keys()), list(xps.values())):
                        newXPS.append([key, value])
                    xps = newXPS
                    del newXPS
                    print(xps)
                    startLevel = 1 if page == 1 else 5 * (page-1) + 1
                    print(startLevel)
                    im = Image.new("RGBA", (1000, 880), bgColor)
                    d = ImageDraw.Draw(im)
                    a = 0
                    y1 = 30
                    y2 = 100
                    guild = self.bot.get_guild(793495102566957096)
                    for pair in xps[startLevel-1:]:
                        print(pair, "pair")
                        if a < 5:
                            user = guild.get_member(int(pair[0]))
                            if not user:
                                xps.remove(pair)
                                x = {}
                                for i in xps:
                                    x.update({i[0]: i[1]})
                                await self.updateXP(OrderedDict(x))
                                continue
                            whitney65 = ImageFont.truetype("assets/fonts/whitney.ttf", 65)
                            await user.avatar_url.save(f"avatar{user.name}.png")
                            avatar = Image.open(f"avatar{user.name}.png", "r").resize((140, 140))
                            im.paste(avatar, (30, y1))
                            os.remove(f"avatar{user.name}.png")
                            d.text((195, y2), f"{startLevel}. {user.name}#{user.discriminator}", fill=textColor, anchor="lm", font=whitney65)
                            startLevel += 1
                            y1 += 170
                            y2 += 170
                            a += 1
                    im.save("levels.png")
                    im.close()
                    embed = discord.Embed(title=f"{get(emojis, name='error')} Refer below!", description="Refer to the message below for the levels.", color=0x36393f)
                    await ctx.send(embed=embed)
                    await ctx.send(file=discord.File(f"levels.png"))
                    time.sleep(3)
                    os.remove("levels.png")
                    curr = "topMenu"

def setup(bot):
    bot.add_cog(Buttons(bot))

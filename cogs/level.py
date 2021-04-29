import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont
import asyncio
import random
import json
import os
import time
from collections import defaultdict, OrderedDict
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864218686488606)
        return defaultdict(int, OrderedDict(reversed(list({k: v for k, v in sorted(json.loads(msg.content).items(), key=lambda item: item[1])}.items()))))
    
    async def updateXP(self, dictionary):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864218686488606)
        dictionary = OrderedDict(reversed(list({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}.items())))
        await msg.edit(content=json.dumps(dictionary, indent=4))
        
    async def getDark(self):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864231847559198)
        return json.loads(msg.content)
    
    async def updateDark(self, dict):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864231847559198)
        await msg.edit(content=json.dumps(dict, indent=4))
    
    @commands.Cog.listener()
    async def on_ready(self):
        global gainedXP
        gainedXP = {}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if "gainedXP" not in globals():
            time.sleep(5)
            return
        if message.channel.id in [817197527496786031, 793550223099691048, 793525460910211104, 793523006172430388, 794999665003069440, 805833182984667197]:
            return
        if message.author.bot:
            return
        try:
            if gainedXP[message.author.id]:
                return
        except KeyError:
            pass
        finally:
            gainedXP[message.author.id] = True
        xps = await self.getXP()
        beforeXP = xps[str(message.author.id)]
        if len(message.content) > 150:
            addXP = 8
        elif len(message.content) >= 121:
            addXP = 7
        elif len(message.content) >= 91:
            addXP = 6
        elif len(message.content) >= 61:
            addXP = 5
        elif len(message.content) >= 31:
            addXP = 4
        elif len(message.content) >= 1:
            addXP = random.randint(2, 3)
        else:
            addXP = 1
        xps[str(message.author.id)] += addXP
        if self.getLevelFromTotalXP(beforeXP) < self.getLevelFromTotalXP(xps[str(message.author.id)]):
            await message.channel.send(f"GG <@{message.author.id}>! You advanced to level **{str(self.getLevelFromTotalXP(xps[str(message.author.id)]))}**!")
            guild = self.bot.get_guild(793495102566957096)
            ranks = {
                3: get(guild.roles, id=795026921749479464),
                10: get(guild.roles, id=795027091141558292),
                15: get(guild.roles, id=795027360126468136),
                25: get(guild.roles, id=795027467126439977)
            }
            if self.getLevelFromTotalXP(xps[str(message.author.id)]) in list(ranks.keys()): # The user has hit the milestone
                await message.author.add_roles(ranks[self.getLevelFromTotalXP(xps[str(message.author.id)])])
                try:
                    await message.author.remove_roles(ranks.values[self.getLevelFromTotalXP(xps[str(message.author.id)])-2])
                except TypeError:
                    pass
        await self.updateXP(xps)
        await asyncio.sleep(30)
        gainedXP[message.author.id] = False
    
    @commands.command()
    async def rank(self, ctx, user: discord.User=None):
        await ctx.send('This may take a while...')
        if not user:
            user = ctx.author
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
        await ctx.send(file=discord.File("rank.png")) 
        os.remove("rank.png")
        
    @commands.command()
    async def updateRankTheme(self, ctx, theme: str):
        if theme not in ["dark", "light"]:
            await ctx.send("You may only choose between `light` and `dark` themes!")
            return
        darks = await self.getDark()
        darks.update({str(ctx.author.id): (theme == "dark")})
        await self.updateDark(darks)
        await ctx.send(f"Your theme has been updated to the {theme} theme!")
        
    @commands.command(name="levels")
    async def levels(self, ctx, page: int=1):
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
            print(pair, "pair nigga")
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
        await ctx.send(file=discord.File(f"levels.png"))
        os.remove("levels.png")
    
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="rank",
                       description="Returns a rank card of yours, or a specified user",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="user",
                               description="the user you want to get a rank card from",
                               option_type=6,
                               required=False
                           )
                       ])
    @commands.command()
    async def _rank(self, ctx: SlashContext, user: discord.User=None):
        await ctx.defer()
        if not user:
            user = ctx.author
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
        im.close()
        await ctx.send("Rank card")
        await ctx.send(file=discord.File("rank.png"))
        time.sleep(3)
        os.remove("rank.png")
        
    @cog_ext.cog_slash(name="updateRankTheme",
                       description="Changes the theme of rank cards for you",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="theme",
                               description="the theme you want to change your rank card to",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="dark",
                                       value="dark"
                                   ),
                                   create_choice(
                                       name="light",
                                       value="light"
                                   )
                               ]
                           )
                       ])
    async def _updateRankTheme(self, ctx: SlashContext, theme: str):
        if theme not in ["dark", "light"]:
            await ctx.send("You may only choose between `light` and `dark` themes!")
            return
        await ctx.defer()
        darks = await self.getDark()
        darks.update({str(ctx.author.id): (theme == "dark")})
        await self.updateDark(darks)
        await ctx.send(f"Your theme has been updated to the {theme} theme!")
        
    @cog_ext.cog_slash(name="levels",
                       description="Returns a leaderboard of levels",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="page",
                               description="the page you want to see, each page is 5 users",
                               option_type=4,
                               required=False
                           )
                       ])
    async def _levels(self, ctx: SlashContext, page: int=1):
        await ctx.defer()
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
            print(pair, "pair nigga")
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
        await ctx.send("Levels")
        await ctx.send(file=discord.File("levels.png"))
        time.sleep(3)
        os.remove("levels.png")
        
def setup(bot):
    bot.add_cog(Level(bot))

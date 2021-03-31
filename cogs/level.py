import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageColor
from functools import lru_cache
import asyncio
import random
from time import sleep

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @lru_cache(maxsize=None)
    def getLevelXP(self, level: int):
        return 5 * (self.getLevelXP(level-1) ** 2) + (50 * self.getLevelXP(level-1)) + 100 if level > 1 else 100
    
    @lru_cache(maxsize=None)
    def getLevelTotalXP(self, level: int):
        return 5 * (self.getLevelXP(level-1) ** 2) + (50 * self.getLevelXP(level-1)) + 100 + self.getLevelXP(level-1) if level > 1 else 100
    
    def getLevelFromTotalXP(self, xp: int):
        n = 1
        while self.getLevelTotalXP(n) < xp:
            n += 1
        return n-1 if self.getLevelTotalXP(n) > xp else n
    
    @commands.Cog.listener()
    async def on_ready(self):
        global gainedXP
        gainedXP = {}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if "gainedXP" not in globals():
            sleep(5)
            return
        if message.channel.id == 817197527496786031:
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
        #xps = await self.getXP()
        try:
            beforeXP = xps[message.author.id]
            xps[message.author.id] += random.randint(4, 6)
        except KeyError:
            beforeXP = 0
            xps[message.author.id] = 0 + random.randint(4, 6)
        finally:
            if self.getLevelFromTotalXP(beforeXP) < self.getLevelFromTotalXP(xps[message.author.id]):
                await message.channel.send(f"GG <@{message.author.id}>! You advanced to level **{int(self.getLevelFromTotalXP(xps[message.author.id]))}**!")
            await self.updateXP(xps)
        await asyncio.sleep(30)
        gainedXP[message.author.id] = False
    
    @commands.command()
    async def rank(self, ctx, user: discord.User=None):
        await ctx.send('Yo')
        if not user:
            user = ctx.author
        dark = True
        if dark:
            textColor = "white"
            bgColor = "#36393f"
        else:
            textColor = "black"
            bgColor = "#ffffff"
        ## Fonts
        rodinpro50 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 50)
        rodinpro80 = ImageFont.truetype("assets/fonts/rodinpro.ttf", 80)
        whitney65 = ImageFont.truetype("assets/fonts/whitney.ttf", 65)
        ## Download avatar
        await ctx.author.avatar_url.save("avatar.png")
        avatar = Image.open("avatar.png", "r")
        ## Background
        im = Image.new("RGBA", (1000, 800), bgColor)
        im.paste(avatar, (30, 30))
        d = ImageDraw.Draw(im)
        d.text((195, 100), f"{user.name}#{user.discriminator}", fill=textColor, anchor="lm", font=whitney65)
        d.text((30, 280), "Level", fill=textColor, anchor="lb", font=rodinpro50)
        d.text((180, 280), "69420", fill=textColor, anchor="lb", font=rodinpro80)
        print("Hi")
        
        def round_corner(radius, fill, x):
            """Draw a round corner"""
            corner = Image.new('RGB', (radius, radius), (54, 57, 63))
            draw = ImageDraw.Draw(corner)
            draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
            return corner
 
        def round_rectangle(size, radius, fill, x):
            """Draw a rounded rectangle"""
            width, height = size
            rectangle = Image.new('RGBA', size, fill)
            corner = round_corner(radius, fill, x)
            rectangle.paste(corner, (0, 0))
            rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
            if x:
                rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                rectangle.paste(corner.rotate(270), (width - radius, 0))
            return rectangle
        
        im.paste(round_rectangle((940, 50), 25, "white", True), (30, 300))
        im.paste(round_rectangle((400, 50), 25, "red", False), (30, 300))
        im.save("out.png") 
        print("Hi2")

def setup(bot):
    bot.add_cog(Level(bot))

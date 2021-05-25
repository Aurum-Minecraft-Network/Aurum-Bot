import discord
from discord.ext import commands
from discord.utils import get
import pyimgur
from decouple import config
import os

class Imgur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imgurid = config("IMGURID")

    @commands.command(name="imgur")
    async def x(self, ctx):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if not ctx.message.attachments:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: No Attachment Found", description="Please attach at least one image!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        links = ""
        for i in ctx.message.attachments:
            if i.filename.endswith((".jpg", ".jpeg", ".png", ".gif")): # Check file type
                await i.save(i.filename) # Download image
                im = pyimgur.Imgur(self.imgurid) # Intialize Pyimgur
                uploaded_image = im.upload_image(os.path.abspath(f"./{i.filename}"), title="Aurum Minecraft Network")
                links += uploaded_image.link + "\n"
                os.remove(os.path.abspath(f"./{i.filename}")) # Delete image to save space
            else:
                embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Attachment Type", description="Accepted types: `jpg`, `jpeg`, `png`, `gif`", color=0x36393f)
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(title=f"{get(emojis, name='imgurdone')} Imgur Upload Successful", description=links, color=0x36393f)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Imgur(bot))

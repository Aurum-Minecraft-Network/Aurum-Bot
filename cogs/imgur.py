import discord
from discord.ext import commands
import pyimgur
from decouple import config
import os

class Imgur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imgurid = config("IMGURID")

    @commands.command(name="imgur")
    async def x(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach at least one image!")
        for i in ctx.message.attachments:
            if i.filename.endswith((".jpg", ".jpeg", ".png", ".gif")): ## Check file type
                msg = "Here is your uploaded image:\n\n"
                await i.save(i.filename) ## Download image
                im = pyimgur.Imgur(self.imgurid) ## Intialize Pyimgur
                uploaded_image = im.upload_image(os.path.abspath(f"./{i.filename}"), title="ATP City")
                msg += f"{uploaded_image.link}\n"
                os.remove(os.path.abspath(f"./{i.filename}")) ## Delete image to save space
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Imgur(bot))

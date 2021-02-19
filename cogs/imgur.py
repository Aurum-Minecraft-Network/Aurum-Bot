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
            return
        msg = "Here is your uploaded image:\n" if len(ctx.message.attachments) == 1 else "Here are your uploaded images:\n"
        for i in ctx.message.attachments:
            if i.filename.endswith((".jpg", ".jpeg", ".png", ".gif")): # Check file type
                await i.save(i.filename) # Download image
                im = pyimgur.Imgur(self.imgurid) # Intialize Pyimgur
                uploaded_image = im.upload_image(os.path.abspath(f"./{i.filename}"), title="ATP City")
                msg += f"{uploaded_image.link}\n"
                os.remove(os.path.abspath(f"./{i.filename}")) # Delete image to save space
        await ctx.send(msg)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.upper().startswith(("[IOM REQUEST]", "**[IOM REQUEST]**", "_[IOM REQUEST]_", "*[IOM REQUEST]*")):
            if not message.attachments:
                await message.channel.send("Invalid request! Please attach at least one image.")
            elif len(message.attachments) > 1:
                await message.channel.send("Invalid request! Please attach only one image.")
            else:
                if message.attachments[0].filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    await message.attachments[0].save(message.attachments[0].filename) # Download image
                    im = pyimgur.Imgur(self.imgurid) # Intialize Pyimgur
                    uploaded_image = im.upload_image(os.path.abspath(f"./{message.attachments[0].filename}"), title="ATP City")
                    os.remove(os.path.abspath(f"./{message.attachments[0].filename}")) # Delete image to save space
                    await message.channel.send(f"Automatically uploaded attached image to Imgur. Link:\n{uploaded_image.link}")
                else:
                    await message.channel.send("Invalid request! Please attach an image file.")

def setup(bot):
    bot.add_cog(Imgur(bot))

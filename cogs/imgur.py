import discord
from discord.ext import commands
from discord.utils import get
import pyimgur
from decouple import config
import os
import datetime


class Imgur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IMGURID = config("IMGURID")

    @commands.command(name="imgur")
    async def imgur_command(self, ctx):
        from cogs.aesthetics import design, embedColor, icons
        emojis = self.bot.get_guild(846318304289488906).emojis
        if not ctx.message.attachments:
            title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
            title += "Error: No Attachment Found"
            embed = discord.Embed(
                title=title,
                description="Please attach at least one image!",
                color=int(embedColor[ctx.author.id], 16),
            )
            if not design[ctx.author.id]:
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.avatar_url,
                )
                embed.set_footer(
                    text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                )
            await ctx.send(embed=embed)
            return
        links = ""
        for i in ctx.message.attachments:
            if i.filename.endswith(
                (".jpg", ".jpeg", ".png", ".gif")
            ):  # Check file type
                await i.save(i.filename)  # Download image
                im = pyimgur.Imgur(self.IMGURID)  # Intialize Pyimgur
                uploaded_image = im.upload_image(
                    os.path.abspath(f"./{i.filename}"), title="Aurum Minecraft Network"
                )
                links += uploaded_image.link + "\n"
                os.remove(
                    os.path.abspath(f"./{i.filename}")
                )  # Delete image to save space
            else:
                title = f"{get(emojis, name='error')} " if icons[ctx.author.id] else ""
                title += "Error: Invalid Attachment Type"
                embed = discord.Embed(
                    title=title,
                    description="Accepted types: `jpg`, `jpeg`, `png`, `gif`",
                    color=int(embedColor[ctx.author.id], 16),
                )
                if not design[ctx.author.id]:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(
                        name=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_footer(
                        text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                    )
                await ctx.send(embed=embed)
                return
        title = f"{get(emojis, name='imgurdone')} " if icons[ctx.author.id] else ""
        title += "Imgur Upload Successful"
        embed = discord.Embed(
            title=title, description=links, color=int(embedColor[ctx.author.id], 16)
        )
        if not design[ctx.author.id]:
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_footer(
                text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Imgur(bot))

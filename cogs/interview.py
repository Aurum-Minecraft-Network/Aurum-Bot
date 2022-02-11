import discord
from discord.errors import NotFound
from discord.ext import commands
from discord.utils import get
import uuid
import string
import random
import os
from constants import EVERYBODY_ROLE_ID
from cogs.aesthetics import get_design, get_embedColor, get_icons
import datetime


class Interview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Function to quickly get the regional indicator emoji given a letter
    def ri(self, letter: str):
        if len(letter) != 1:
            raise ValueError("You should only pass a single letter.")
        else:
            if letter.lower() not in string.ascii_lowercase:
                raise ValueError("You should only pass a letter.")
            else:
                return f":regional_indicator_{letter.lower()}:"

    @commands.command()
    async def interview(self, ctx):
        guild = self.bot.get_guild(793495102566957096)
        intID = str(uuid.uuid4())
        newInt = await guild.create_text_channel(f"int-{intID}")
        await newInt.edit(category=get(guild.channels, id=833648963197599754))
        perms = newInt.overwrites_for(ctx.author)
        perms.read_messages = True
        perms.send_messages = True
        await newInt.set_permissions(ctx.author, overwrite=perms)
        perms = newInt.overwrites_for(guild.default_role)
        perms.read_messages = False
        await newInt.set_permissions(guild.default_role, overwrite=perms)
        perms = newInt.overwrites_for(get(guild.roles, id=EVERYBODY_ROLE_ID))
        perms.read_messages = False
        await newInt.set_permissions(
            get(guild.roles, id=EVERYBODY_ROLE_ID), overwrite=perms
        )
        emojis = self.bot.get_guild(846318304289488906).emojis
        title = (
            f"{get(emojis, name='success')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Channel created successfully"
        embed = discord.Embed(
            title=title,
            description=f"Channel created at <#{newInt.id}>. Please move!",
            color=int(get_embedColor()[str(ctx.author.id)], 16),
        )
        if not get_design()[str(ctx.author.id)]:
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_footer(
                text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
            )
        await ctx.send(embed=embed)

        async def wait_until_done():
            await newInt.send(
                'Remember, type "[DONE]" to proceed to the next question.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[DONE]",
            )  # Wait until the interviewee says [DONE]

        await newInt.send("Welcome to this interview session!")
        await newInt.send(
            "Please note that all messages sent in this channel will be logged for future reference."
        )
        msg = await newInt.send(
            f"""If you agree, please choose from the following list by reacting to the message:
                           
**APPLY FOR:**
{self.ri("g")} Graphic Designer
{self.ri("a")} Administrator
{self.ri("b")} City Builder

:no_entry: **__DO NOT REACT YET__**"""
        )
        await msg.add_reaction("🇬")
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        await msg.edit(
            content=f"""If you agree, please choose from the following list by reacting to the message:
                           
**APPLY FOR:**
{self.ri("g")} Graphic Designer
{self.ri("a")} Administrator
{self.ri("b")} City Builder

:white_check_mark: **__REACT NOW__**"""
        )
        payload = await self.bot.wait_for(
            "raw_reaction_add",
            check=lambda payload: payload.message_id == msg.id
            and payload.user_id == ctx.author.id,
        )
        pass
        if payload.emoji.name == "🇦":
            await newInt.send(
                "Thank you for applying for Administrator!"
            )
            await newInt.send("A number of questions will be asked.")
            await newInt.send(
                "After the question has been asked, you may use an unlimited amount of messages, and an unlimited amount of time to answer the question."
            )
            await newInt.send(
                'When you are sure about the answer, type "[DONE]" to proceed to the next question.'
            )
            await newInt.send(f"""Interview ID for reference: `{intID}`""")
            await newInt.send(
                'You may raise questions now. Otherwise, type "[BEGIN]" to begin the interview process.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[BEGIN]",
            )  # Wait until the interviewee says [BEGIN]
            await newInt.send("Firstly, please tell us your Minecraft username.")
            await wait_until_done()
            await newInt.send(
                "Please briefly explain why would you like to become a Administrator."
            )
            await wait_until_done()
            await newInt.send(
                "What would you do for the server, if you successfully become a Administrator?"
            )
            await wait_until_done()
            await newInt.send(
                'The interview process has ended. Please raise any questions that you have now, otherwise, type "[END]" to archive this channel and await processing.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[END]",
            )  # Wait until the interviewee says [END]
            perms = newInt.overwrites_for(ctx.author)
            perms.read_messages = True
            perms.send_messages = False
            await newInt.set_permissions(ctx.author, overwrite=perms)
            perms = newInt.overwrites_for(guild.default_role)
            perms.read_messages = False
            await newInt.set_permissions(guild.default_role, overwrite=perms)
            perms = newInt.overwrites_for(get(guild.roles, id=EVERYBODY_ROLE_ID))
            perms.read_messages = False
            await newInt.edit(
                category=get(guild.channels, id=817798276366991371),
                name=f"int-ar-{intID}",
            )
        elif payload.emoji.name == "🇬":
            await newInt.send("Thank you for applying for Graphic Designer!")
            await newInt.send("A number of questions will be asked.")
            await newInt.send(
                "After the question has been asked, you may use an unlimited amount of messages, and an unlimited amount of time to answer the question."
            )
            await newInt.send(
                'When you are sure about the answer, type "[DONE]" to proceed to the next question.'
            )
            await newInt.send(f"""Interview ID for reference: `{intID}`""")
            await newInt.send(
                'You may raise questions now. Otherwise, type "[BEGIN]" to begin the interview process.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[BEGIN]",
            )  # Wait until the interviewee says [BEGIN]
            await newInt.send("Firstly, please tell us your Minecraft username.")
            await wait_until_done()
            await newInt.send(
                "What image editing programs can you use?\ne.g. Adobe Photoshop, paint.net, Adobe Illustrator, GIMP"
            )
            await wait_until_done()
            await newInt.send(
                "If applicable, describe your style of art/ images you make\ne.g. minimalistic, cartoony"
            )
            await wait_until_done()
            await newInt.send(
                "If you want, you may send some fantastic work of yours to us now! Note that this is not mandatory."
            )
            await newInt.send(
                'The interview process has ended. Please raise any questions that you have now, otherwise, type "[END]" to archive this channel and await processing.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[END]",
            )  # Wait until the interviewee says [END]
            perms = newInt.overwrites_for(ctx.author)
            perms.read_messages = True
            perms.send_messages = False
            await newInt.set_permissions(ctx.author, overwrite=perms)
            perms = newInt.overwrites_for(guild.default_role)
            perms.read_messages = False
            await newInt.set_permissions(guild.default_role, overwrite=perms)
            perms = newInt.overwrites_for(get(guild.roles, id=EVERYBODY_ROLE_ID))
            perms.read_messages = False
            await newInt.edit(
                category=get(guild.channels, id=817798276366991371),
                name=f"int-ar-{intID}",
            )
        elif payload.emoji.name == "🇧":
            await newInt.send("Thank you for applying for City Builder!")
            await newInt.send("A number of questions will be asked.")
            await newInt.send(
                "After the question has been asked, you may use an unlimited amount of messages, and an unlimited amount of time to answer the question."
            )
            await newInt.send(
                'When you are sure about the answer, type "[DONE]" to proceed to the next question.'
            )
            await newInt.send(f"""Interview ID for reference: `{intID}`""")
            await newInt.send(
                'You may raise questions now. Otherwise, type "[BEGIN]" to begin the interview process.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[BEGIN]",
            )  # Wait until the interviewee says [BEGIN]
            await newInt.send("Firstly, please tell us your Minecraft username.")
            await wait_until_done()
            await newInt.send(
                "Please briefly explain why you want access WorldEdit features."
            )
            await wait_until_done()
            await newInt.send(
                "Now, show us what you have built!\nThis does not affect your application status; we are just curious on what you have built! Feel free to show us! Note that this is not mandatory."
            )
            await wait_until_done()
            await newInt.send(
                'The interview process has ended. Please raise any questions that you have now, otherwise, type "[END]" to archive this channel and await processing.'
            )
            await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author
                and message.content == "[END]",
            )  # Wait until the interviewee says [END]
            perms = newInt.overwrites_for(ctx.author)
            perms.read_messages = True
            perms.send_messages = False
            await newInt.set_permissions(ctx.author, overwrite=perms)
            perms = newInt.overwrites_for(guild.default_role)
            perms.read_messages = False
            await newInt.set_permissions(guild.default_role, overwrite=perms)
            perms = newInt.overwrites_for(get(guild.roles, id=EVERYBODY_ROLE_ID))
            perms.read_messages = False
            await newInt.edit(
                category=get(guild.channels, id=817798276366991371),
                name=f"int-ar-{intID}",
            )

    @commands.command()
    async def approve(self, ctx, id, reason: str = None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        guild = self.bot.get_guild(793495102566957096)
        channel = get(guild.channels, name=f"int-ar-{id}")
        if not channel:
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Argument"
            embed = discord.Embed(
                title=title,
                description="The ID is invalid!",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            if not get_design()[str(ctx.author.id)]:
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
        messages = await channel.history(limit=50).flatten()
        for message in messages:
            if message.content == "[END]":
                target = message.author
                break
        else:
            messages = await channel.history().flatten()
            for message in messages:
                if message.content == "[END]":
                    target = message.author
                    break
            else:
                raise NotFound("Can't find [END] statement!")
        dm = await target.create_dm()
        title = f"{get(emojis, name='success')} " if get_icons()[str(target.id)] else ""
        title += "Your interview application has been approved!"
        desc = f"**Reason:** {reason}" if reason else "No reason provided"
        desc += f"\n\n**Interview ID:** {id}"
        embed = discord.Embed(
            title=title,
            description=desc,
            color=int(get_embedColor()[str(target.id)], 16),
        )
        if not get_design()[str(target.id)]:
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(
                name=f"{target.name}#{target.discriminator}",
                icon_url=target.avatar_url,
            )
            embed.set_footer(
                text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
            )
        await dm.send(embed=embed)

    @commands.command()
    async def reject(self, ctx, id, *, reason: str = None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        guild = self.bot.get_guild(793495102566957096)
        channel = get(guild.channels, name=f"int-ar-{id}")
        if not channel:
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Argument"
            embed = discord.Embed(
                title=title,
                description="The ID is invalid!",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            if not get_design()[str(ctx.author.id)]:
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
        messages = await channel.history(limit=50).flatten()
        for message in messages:
            if message.content == "[END]":
                target = message.author
                break
        else:
            messages = await channel.history().flatten()
            for message in messages:
                if message.content == "[END]":
                    target = message.author
                    break
            else:
                raise NotFound("Can't find [END] statement!")
        dm = await target.create_dm()
        title = f"{get(emojis, name='reject')} " if get_icons()[str(target.id)] else ""
        title += "Your interview application has been rejected!"
        desc = f"**Reason:** {reason}" if reason else "No reason provided"
        desc += f"\n\n**Interview ID:** {id}"
        embed = discord.Embed(
            title=title,
            description=desc,
            color=int(get_embedColor()[str(target.id)], 16),
        )
        if not get_design()[str(target.id)]:
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(
                name=f"{target.name}#{target.discriminator}",
                icon_url=target.avatar_url,
            )
            embed.set_footer(
                text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
            )
        await dm.send(embed=embed)


def setup(bot):
    bot.add_cog(Interview(bot))

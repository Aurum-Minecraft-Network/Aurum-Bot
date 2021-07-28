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
from decouple import config
import boto3
import datetime

## AWS setup
key = config("AWSKEY")  # AWS Access Key ID
secret = config("AWSSECRET")  # AWS Secret Access Key
client = boto3.client(
    "s3", aws_access_key_id=key, aws_secret_access_key=secret
)  # Initialize boto3 client


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_level_xp(self, level: int):
        return 5 * ((level - 1) ** 2) + (50 * (level - 1)) + 100 if level > 1 else 100

    def get_level_total_xp(self, level: int):
        xp = 0
        while level > 0:
            xp += self.get_level_xp(level)
            level -= 1
        return xp

    def get_level_from_total_xp(self, xp: int):
        n = 1
        a = self.get_level_total_xp(n)
        while a < xp:
            n += 1
            a = self.get_level_total_xp(n)
        return n - 1 if a > xp else n

    async def get_xp(self):
        return defaultdict(
            int,
            OrderedDict(
                reversed(
                    list(
                        {
                            k: v
                            for k, v in sorted(
                                json.loads(
                                    client.get_object(
                                        Bucket="atpcitybot", Key="xps.json"
                                    )["Body"].read()
                                ).items(),
                                key=lambda item: item[1],
                            )
                        }.items()
                    )
                )
            ),
        )

    async def update_xp(self, dictionary):
        dictionary = OrderedDict(
            reversed(
                list(
                    {
                        k: v
                        for k, v in sorted(dictionary.items(), key=lambda item: item[1])
                    }.items()
                )
            )
        )
        with open("xps.json", "w") as f:
            json.dump(dictionary, f, indent=4)
        with open("xps.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "xps.json")

    async def get_dark(self):
        channel = self.bot.get_channel(797745275253817354)
        msg = await channel.fetch_message(826864231847559198)
        return json.loads(msg.content)

    async def update_dark(self, dict):
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
        if message.guild.id != 793495102566957096:
            return
        if message.channel.id in [
            817197527496786031,
            793550223099691048,
            793525460910211104,
            793523006172430388,
            794999665003069440,
            805833182984667197,
            837715004991340555,
        ]:
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
        xps = await self.get_xp()
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
        if self.get_level_from_total_xp(beforeXP) < self.get_level_from_total_xp(
            xps[str(message.author.id)]
        ):
            emojis = self.bot.get_guild(846318304289488906).emojis
            from cogs.aesthetics import get_design, get_embedColor, get_icons

            title = (
                f"{get(emojis, name='lvup')} "
                if get_icons()[str(message.author.id)]
                else ""
            )
            title += f"GG {message.author.name}!"
            embed = discord.Embed(
                title=title,
                description=f"You advanced to level **{str(self.get_level_from_total_xp(xps[str(message.author.id)]))}**!",
                color=int(get_embedColor()[message.author.id], 16),
            )
            if not get_design()[message.author.id]:
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(
                    name=f"{message.author.name}#{message.author.discriminator}",
                    icon_url=message.author.avatar_url,
                )
                embed.set_footer(
                    text="Aurum Bot", icon_url="https://i.imgur.com/sePqvZX.png"
                )
            await message.channel.send(embed=embed)
            guild = self.bot.get_guild(793495102566957096)
            ranks = {
                3: get(guild.roles, id=795026921749479464),
                10: get(guild.roles, id=795027091141558292),
                15: get(guild.roles, id=795027360126468136),
                25: get(guild.roles, id=795027467126439977),
            }
            if self.get_level_from_total_xp(xps[str(message.author.id)]) in list(
                ranks.keys()
            ):  # The user has hit the milestone
                await message.author.add_roles(
                    ranks[self.get_level_from_total_xp(xps[str(message.author.id)])]
                )
                try:
                    await message.author.remove_roles(
                        ranks.values[
                            self.get_level_from_total_xp(xps[str(message.author.id)])
                            - 2
                        ]
                    )
                except TypeError:
                    pass
        await self.update_xp(xps)
        await asyncio.sleep(30)
        gainedXP[message.author.id] = False

    @commands.command()
    async def rank(self, ctx, user: discord.User = None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        title = (
            f"{get(emojis, name='wait')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Please wait..."
        embed = discord.Embed(
            title=title,
            description="This may take a while...",
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
        if not user:
            user = ctx.author
        try:
            dark = (await self.get_dark())[str(ctx.author.id)]
        except KeyError:
            darks = await self.get_dark()
            darks.update({str(ctx.author.id): True})
            await self.update_dark(darks)
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
        xps = await self.get_xp()
        level = self.get_level_from_total_xp(xps[str(user.id)])
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
        d.text(
            (195, 100),
            f"{user.name}#{user.discriminator}",
            fill=textColor,
            anchor="lm",
            font=whitney65,
        )
        d.text((30, 430), "Rank", fill=textColor, anchor="lb", font=rodinpro50)
        d.text(
            (170, 430), "#" + str(rank), fill=textColor, anchor="lb", font=rodinpro80
        )
        d.text((30, 280), "Level", fill=textColor, anchor="lb", font=rodinpro50)
        d.text((180, 280), str(level), fill=textColor, anchor="lb", font=rodinpro80)

        def round_corner(radius, fill):
            """Draw a round corner"""
            corner = Image.new("RGB", (radius, radius), bgColor)
            draw = ImageDraw.Draw(corner)
            draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
            return corner

        def round_rectangle(size, radius, fill, x):
            """Draw a rounded rectangle"""
            width, height = size
            rectangle = Image.new("RGBA", size, fill)
            corner = round_corner(radius, fill)
            rectangle.paste(corner, (0, 0))
            rectangle.paste(
                corner.rotate(90), (0, height - radius)
            )  # Rotate the corner and paste it
            if x:
                rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                rectangle.paste(corner.rotate(270), (width - radius, 0))
            return rectangle

        xp = xps[str(user.id)] - self.get_level_total_xp(level)  # Current level XP
        targetxp = self.get_level_xp(level + 1)

        im.paste(round_rectangle((940, 50), 25, barColor, True), (30, 300))
        im.paste(
            round_rectangle((round(940 * (xp / targetxp)), 50), 25, "blue", False),
            (30, 300),
        )

        d.text(
            (970, 280),
            f"{xp} / {targetxp} XP",
            fill=textColor,
            anchor="rb",
            font=rodinpro50,
        )
        im.save("rank.png")
        await ctx.send(file=discord.File("rank.png"))
        os.remove("rank.png")

    @commands.command(name="updateRankTheme")
    async def update_rank_theme(self, ctx, theme: str):
        emojis = self.bot.get_guild(846318304289488906).emojis
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        if theme not in ["dark", "light"]:
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Argument"
            embed = discord.Embed(
                title=title,
                description="You may only choose between `light` and `dark` themes!",
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
        darks = await self.get_dark()
        darks.update({str(ctx.author.id): (theme == "dark")})
        await self.update_dark(darks)
        if theme == "light":
            title = (
                f"{get(emojis, name='success')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Update Successful"
            embed = discord.Embed(
                title=title,
                description=f"{get(emojis, name='lightmode')} Your theme has been updated to the light theme!",
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
        else:
            title = (
                f"{get(emojis, name='success')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Update Successful"
            embed = discord.Embed(
                title=title,
                description=f"{get(emojis, name='darkmode')} Your theme has been updated to the dark theme!",
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

    @commands.command()
    async def levels(self, ctx, page: int = 1):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        
        start_index = (page-1) * 15
        
        xps = [[key, value] for key, value in zip(list((await self.get_xp()).keys()), list((await self.get_xp()).values()))]
        xpsList = xps[start_index:start_index+15]
        
        none_user_found = True
        
        ## Imagine if this could be a do-while loop
        while none_user_found:
            res = ""
            none_user_found = False
            for rank, pair in enumerate(xpsList):
                user = self.bot.get_user(int(pair[0]))
                if not user:
                    none_user_found = True
                    xps.remove(pair)
                    xpsList = xps[start_index:start_index+15]
                    break
                res += f"**{rank+1+start_index}.** {user.name}#{user.discriminator} - Level __{self.get_level_from_total_xp(int(pair[1]))}__\n"
        
        title = (
            f"{get(emojis, name='leaderboard')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "XP Leaderboard"
        embed = discord.Embed(
            title=title,
            description=res,
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
        
    ### SLASH COMMANDS ZONE ###

    guildID = 793495102566957096

    @cog_ext.cog_slash(
        name="rank",
        description="Returns a rank card of yours, or a specified user",
        guild_ids=[guildID],
        options=[
            create_option(
                name="user",
                description="the user you want to get a rank card from",
                option_type=6,
                required=False,
            )
        ],
    )
    @commands.command()
    async def _rank(self, ctx: SlashContext, user: discord.User = None):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        title = (
            f"{get(emojis, name='wait')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Please wait..."
        embed = discord.Embed(
            title=title,
            description="This may take a while...",
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
        if not user:
            user = ctx.author
        try:
            dark = (await self.get_dark())[str(ctx.author.id)]
        except KeyError:
            darks = await self.get_dark()
            darks.update({str(ctx.author.id): True})
            await self.update_dark(darks)
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
        xps = await self.get_xp()
        level = self.get_level_from_total_xp(xps[str(user.id)])
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
        d.text(
            (195, 100),
            f"{user.name}#{user.discriminator}",
            fill=textColor,
            anchor="lm",
            font=whitney65,
        )
        d.text((30, 430), "Rank", fill=textColor, anchor="lb", font=rodinpro50)
        d.text(
            (170, 430), "#" + str(rank), fill=textColor, anchor="lb", font=rodinpro80
        )
        d.text((30, 280), "Level", fill=textColor, anchor="lb", font=rodinpro50)
        d.text((180, 280), str(level), fill=textColor, anchor="lb", font=rodinpro80)

        def round_corner(radius, fill):
            """Draw a round corner"""
            corner = Image.new("RGB", (radius, radius), bgColor)
            draw = ImageDraw.Draw(corner)
            draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
            return corner

        def round_rectangle(size, radius, fill, x):
            """Draw a rounded rectangle"""
            width, height = size
            rectangle = Image.new("RGBA", size, fill)
            corner = round_corner(radius, fill)
            rectangle.paste(corner, (0, 0))
            rectangle.paste(
                corner.rotate(90), (0, height - radius)
            )  # Rotate the corner and paste it
            if x:
                rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                rectangle.paste(corner.rotate(270), (width - radius, 0))
            return rectangle

        xp = xps[str(user.id)] - self.get_level_total_xp(level)  # Current level XP
        targetxp = self.get_level_xp(level + 1)

        im.paste(round_rectangle((940, 50), 25, barColor, True), (30, 300))
        im.paste(
            round_rectangle((round(940 * (xp / targetxp)), 50), 25, "blue", False),
            (30, 300),
        )

        d.text(
            (970, 280),
            f"{xp} / {targetxp} XP",
            fill=textColor,
            anchor="rb",
            font=rodinpro50,
        )
        im.save("rank.png")
        await ctx.send(file=discord.File("rank.png"))
        os.remove("rank.png")

    @cog_ext.cog_slash(
        name="updateRankTheme",
        description="Changes the theme of rank cards for you",
        guild_ids=[guildID],
        options=[
            create_option(
                name="theme",
                description="the theme you want to change your rank card to",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="dark", value="dark"),
                    create_choice(name="light", value="light"),
                ],
            )
        ],
    )
    async def _update_rank_theme(self, ctx: SlashContext, theme: str):
        await ctx.defer()
        emojis = self.bot.get_guild(846318304289488906).emojis
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        if theme not in ["dark", "light"]:
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Argument"
            embed = discord.Embed(
                title=title,
                description="You may only choose between `light` and `dark` themes!",
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
        darks = await self.get_dark()
        darks.update({str(ctx.author.id): (theme == "dark")})
        await self.update_dark(darks)
        if theme == "light":
            title = (
                f"{get(emojis, name='success')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Update Successful"
            embed = discord.Embed(
                title=title,
                description=f"{get(emojis, name='lightmode')} Your theme has been updated to the light theme!",
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
        else:
            title = (
                f"{get(emojis, name='success')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Update Successful"
            embed = discord.Embed(
                title=title,
                description=f"{get(emojis, name='darkmode')} Your theme has been updated to the dark theme!",
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

    @cog_ext.cog_slash(
        name="levels",
        description="Returns a leaderboard of levels",
        guild_ids=[guildID],
        options=[
            create_option(
                name="page",
                description="the page you want to see, each page is 5 users",
                option_type=4,
                required=False,
            )
        ],
    )
    async def _levels(self, ctx: SlashContext, page: int = 1):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        await ctx.defer()
        emojis = self.bot.get_guild(846318304289488906).emojis
        
        start_index = (page-1) * 15
        
        xps = [[key, value] for key, value in zip(list((await self.get_xp()).keys()), list((await self.get_xp()).values()))]
        xpsList = xps[start_index:start_index+15]
        
        none_user_found = True
        
        ## Imagine if this could be a do-while loop
        while none_user_found:
            res = ""
            none_user_found = False
            for rank, pair in enumerate(xpsList):
                user = self.bot.get_user(int(pair[0]))
                if not user:
                    none_user_found = True
                    xps.remove(pair)
                    xpsList = xps[start_index:start_index+15]
                    break
                res += f"**{rank+1+start_index}.** {user.name}#{user.discriminator} - Level __{self.get_level_from_total_xp(int(pair[1]))}__\n"
        
        title = (
            f"{get(emojis, name='leaderboard')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "XP Leaderboard"
        embed = discord.Embed(
            title=title,
            description=res,
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


def setup(bot):
    bot.add_cog(Level(bot))

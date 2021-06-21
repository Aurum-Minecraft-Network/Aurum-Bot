import datetime
from constants import AURUM_ASSET_SERVER_ID
from typing import Union
import discord
from discord.ext import commands, tasks
from decouple import config
import boto3
import json
import re
from discord.utils import get

from discord_slash.context import SlashContext

## AWS setup
KEY = config("AWSKEY")  # AWS Access Key ID
SECRET = config("AWSSECRET")  # AWS Secret Access Key
client = boto3.client(
    "s3", aws_access_key_id=KEY, aws_secret_access_key=SECRET
)  # Initialize boto3 client

design = json.loads(
    client.get_object(Bucket="atpcitybot", Key="design.json")["Body"].read()
)

embedColor = json.loads(
    client.get_object(Bucket="atpcitybot", Key="embedColor.json")["Body"].read()
)
icons = json.loads(
    client.get_object(Bucket="atpcitybot", Key="icons.json")["Body"].read()
)


def get_design():
    with open("design.json", "r") as f:
        return json.load(f)


def get_embedColor():
    with open("embedColor.json", "r") as f:
        return json.load(f)


def get_icons():
    with open("icons.json", "r") as f:
        return json.load(f)


class Aesthetics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.design = design
        self.embedColor = embedColor
        self.icons = icons
        self.get_latest_values.start()
        # self.fix_missing_members.start()

    async def send_no_permission(
        self,
        ctx: Union[
            discord.ext.commands.Context,
            SlashContext,
            discord.TextChannel,
            discord.DMChannel,
            discord.GroupChannel,
        ],
    ):
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        title = (
            f"{get(emojis, name='error')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Error: No Permission"
        embed = discord.Embed(
            title=title,
            description="Sorry, but you don't have permission to do that.",
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

    @tasks.loop(seconds=45)
    async def get_latest_values(self):
        global design, embedColor, icons
        design = json.loads(
            client.get_object(Bucket="atpcitybot", Key="design.json")["Body"].read()
        )
        embedColor = json.loads(
            client.get_object(Bucket="atpcitybot", Key="embedColor.json")["Body"].read()
        )
        icons = json.loads(
            client.get_object(Bucket="atpcitybot", Key="icons.json")["Body"].read()
        )
        with open("design.json", "w") as f:
            json.dump(design, f, indent=4)
        with open("embedColor.json", "w") as f:
            json.dump(embedColor, f, indent=4)
        with open("icons.json", "w") as f:
            json.dump(icons, f, indent=4)

    @get_latest_values.before_loop
    async def before_get_latest_values(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 793495102566957096:
            return
        self.design.update({str(member.id): True})
        self.embedColor.update({str(member.id): "36393f"})
        self.icons.update({str(member.id): True})
        with open("design.json", "w") as f:
            json.dump(self.design, f, indent=4)
        with open("design.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "design.json")
        with open("embedColor.json", "w") as f:
            json.dump(self.embedColor, f, indent=4)
        with open("embedColor.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "embedColor.json")
        with open("icons.json", "w") as f:
            json.dump(self.icons, f, indent=4)
        with open("icons.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "icons.json")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != 793495102566957096:
            return
        self.design.remove(str(member.id))
        self.embedColor.remove(str(member.id))
        self.icons.remove(str(member.id))
        with open("design.json", "w") as f:
            json.dump(self.design, f, indent=4)
        with open("design.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "design.json")
        with open("embedColor.json", "w") as f:
            json.dump(self.embedColor, f, indent=4)
        with open("embedColor.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "embedColor.json")
        with open("icons.json", "w") as f:
            json.dump(self.icons, f, indent=4)
        with open("icons.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "icons.json")

    @commands.command()
    async def customize(self, ctx, arg1: str, *, arg2: str):
        if arg1 == "design":
            if arg2 == "simple":
                self.design.update({str(ctx.author.id): True})
                with open("design.json", "w") as f:
                    json.dump(self.design, f, indent=4)
                with open("design.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "design.json")
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='success')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Design Language Updated"
                embed = discord.Embed(
                    title=title,
                    description=f"Updated design language to `{arg2}`.",
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
            elif arg2 == "detailed":
                self.design.update({str(ctx.author.id): False})
                with open("design.json", "w") as f:
                    json.dump(self.design, f, indent=4)
                with open("design.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "design.json")
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='success')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Design Language Updated"
                embed = discord.Embed(
                    title=title,
                    description=f"Updated design language to `{arg2}`.",
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
            else:
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='error')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Error: Invalid Argument"
                embed = discord.Embed(
                    title=title,
                    description="You may only choose from `simple` or `detailed` design languages.",
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
        elif arg1 == "embedColor":
            if not re.fullmatch("[a-f,A-F,0-9]{6}", arg2):
                if arg2 == "dark":
                    arg2 = "36393f"
                elif arg2 == "light":
                    arg2 = "ffffff"
                elif arg2 == "orange":
                    arg2 = "ffb000"
                else:
                    from cogs.aesthetics import get_design, get_embedColor, get_icons

                    emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                    title = (
                        f"{get(emojis, name='error')} "
                        if get_icons()[str(ctx.author.id)]
                        else ""
                    )
                    title += "Error: Invalid Argument"
                    embed = discord.Embed(
                        title=title,
                        description="You may only choose from `dark`, `light`, `orange`, or input a valid color hex (e.g. `ff0000`).",
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
            self.embedColor.update({str(ctx.author.id): arg2.lower()})
            with open("embedColor.json", "w") as f:
                json.dump(self.embedColor, f, indent=4)
            with open("embedColor.json", "rb") as f:
                client.upload_fileobj(f, "atpcitybot", "embedColor.json")
            from cogs.aesthetics import get_design, get_embedColor, get_icons

            emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
            title = (
                f"{get(emojis, name='success')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Embed Sidebar Color Updated"
            embed = discord.Embed(
                title=title,
                description=f"Color updated to `#{arg2.lower()}`.",
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
        elif arg1 == "icons":
            if arg2.lower() in ["true", "false"]:
                self.icons.update({str(ctx.author.id): arg2.lower() == "true"})
                with open("icons.json", "w") as f:
                    json.dump(self.icons, f, indent=4)
                with open("icons.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "icons.json")
                from cogs.aesthetics import get_design, get_embedColor, get_icons

                emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
                title = (
                    f"{get(emojis, name='success')} "
                    if get_icons()[str(ctx.author.id)]
                    else ""
                )
                title += "Icons Preference Updated"
                embed = discord.Embed(
                    title=title,
                    description="Icons will now show up in the bot's messages."
                    if arg2.lower() == "true"
                    else "Icons will now not show up in the bot's messages.",
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
            from cogs.aesthetics import get_design, get_embedColor, get_icons

            emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
            title = (
                f"{get(emojis, name='error')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Error: Invalid Argument"
            embed = discord.Embed(
                title=title,
                description="You may only choose from `true` or `false`!",
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

    @tasks.loop(seconds=20)
    async def fix_missing_members(self):
        guild = self.bot.get_guild(793495102566957096)
        design = get_design()
        embedColor = get_embedColor()
        icons = get_icons()
        for member in guild.members:
            if member.id not in design:
                design.update({str(member.id): True})
            if member.id not in embedColor:
                embedColor.update({str(member.id): "36393f"})
            if member.id not in icons:
                icons.update({str(member.id): True})
        with open("design.json", "w") as f:
            json.dump(design, f, indent=4)
        with open("design.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "design.json")
        with open("embedColor.json", "w") as f:
            json.dump(embedColor, f, indent=4)
        with open("embedColor.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "embedColor.json")
        with open("icons.json", "w") as f:
            json.dump(icons, f, indent=4)
        with open("icons.json", "rb") as f:
            client.upload_fileobj(f, "atpcitybot", "icons.json")

    @fix_missing_members.before_loop
    async def before_fixMissingMembers(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def sync_members(self, ctx):
        if ctx.author.id != 438298127225847810:
            await self.send_no_permission(ctx=ctx)
            return
        emojis = self.bot.get_guild(AURUM_ASSET_SERVER_ID).emojis
        title = (
            f"{get(emojis, name='async')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Adding missing entries to aesthetic preference files"
        embed = discord.Embed(
            title=title,
            description="Please wait...",
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
        msg = await ctx.send(embed=embed)
        await self.fixMissingMembers.__call__()
        title = (
            f"{get(emojis, name='success')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Missing entries added to aesthetic preference files"
        embed = discord.Embed(
            title=title,
            description="Operation successful.",
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
        await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Aesthetics(bot))

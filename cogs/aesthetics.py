import discord
from discord.ext import commands, tasks
from decouple import config
import boto3
import json
import re

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


class Aesthetics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.design = design
        self.embedColor = embedColor
        self.icons = icons
        self.get_latest_values.start()
        # self.fix_missing_members.start()

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
            elif arg2 == "detailed":
                self.design.update({str(ctx.author.id): False})
                with open("design.json", "w") as f:
                    json.dump(self.design, f, indent=4)
                with open("design.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "design.json")
            else:
                pass
                return
        elif arg1 == "embedColor":
            if not re.fullmatch("[a-f,A-F,0-9]{6}", arg2):
                if arg1 == "dark":
                    arg1 = "36393f"
                elif arg1 == "light":
                    arg1 = "ffffff"
                else:
                    pass
                    return
            else:
                self.embedColor.update({str(ctx.author.id): arg2.lower()})
                with open("embedColor.json", "w") as f:
                    json.dump(self.embedColor, f, indent=4)
                with open("embedColor.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "embedColor.json")
        elif arg1 == "icons":
            if arg1.lower() in ["true", "false"]:
                self.icons.update({str(ctx.author.id): arg1.lower() == "true"})
                with open("icons.json", "w") as f:
                    json.dump(self.icons, f, indent=4)
                with open("icons.json", "rb") as f:
                    client.upload_fileobj(f, "atpcitybot", "icons.json")

    @tasks.loop(seconds=20)
    async def fix_missing_members(self):
        guild = self.bot.get_guild(793495102566957096)
        for member in guild.members:
            if member.id not in self.design:
                self.design.update({str(member.id): True})
            if member.id not in self.embedColor:
                self.embedColor.update({str(member.id): "36393f"})
            if member.id not in self.icons:
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

    @fix_missing_members.before_loop
    async def before_fixMissingMembers(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def sync_members(self, ctx):
        if ctx.author.id != 438298127225847810:
            pass
            return
        await self.fixMissingMembers.__call__()


def setup(bot):
    bot.add_cog(Aesthetics(bot))

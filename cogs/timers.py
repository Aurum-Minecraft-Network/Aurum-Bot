import discord
from discord.ext import commands
from constants import GENERAL_CHANNEL_ID, COMMANDS_CHANNEL_ID, MINECRAFT_SERVER_CHAT_ID


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Initializes variables."""
        global gen_count, mine_count
        gen_count = 0
        mine_count = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == GENERAL_CHANNEL_ID:
            global gen_count
            gen_count += 1
            if gen_count == 50:
                gen_count = 0
                embed1 = discord.Embed(
                    title="Server IP",
                    description="If you need the IP, refer here.\nhttps://github.com/Aurum-Minecraft-Network/How-To-Join/wiki",
                    color=0xFFB000,
                )
                embed2 = discord.Embed(
                    title="Want to help us grow?",
                    description=f"Then use `a!interview` in <#{COMMANDS_CHANNEL_ID}>! We are waiting for you!",
                    color=0xFFB000,
                )
                await message.channel.send(embed=embed1)
                await message.channel.send(embed=embed2)
        elif message.channel.id == MINECRAFT_SERVER_CHAT_ID:
            global mine_count
            mine_count += 1
            if mine_count == 50:
                mine_count == 0
                embed = discord.Embed(
                    title="Server IP",
                    description="If you need the IP, refer here.\nhttps://github.com/Aurum-Minecraft-Network/How-To-Join/wiki",
                    color=0xFFB000,
                )
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Timers(bot))

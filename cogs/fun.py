import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.utils import get
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['da'])
    async def defaultAvatar(self, ctx, *, user: discord.Member=None):
        if user:
            remainder = int(user.discriminator) % 5
            pronoun = f"{user.name} has"
        else:
            remainder = int(ctx.author.discriminator) % 5 
            pronoun = "You have"
        if remainder == 0:
            color = "blurple"
            colorh = 0x7289DA
            link = "https://cdn.discordapp.com/embed/avatars/0.png"
        elif remainder == 1:
            color = "gray"
            colorh = 0x747F8D
            link = "https://cdn.discordapp.com/embed/avatars/1.png"
        elif remainder == 2:
            color = "green"
            colorh = 0x43B581
            link = "https://cdn.discordapp.com/embed/avatars/2.png"
        elif remainder == 3:
            color = "yellow"
            colorh = 0xFAA61A
            link = "https://cdn.discordapp.com/embed/avatars/3.png"
        elif remainder == 4:
            color = "red"
            colorh = 0xF04747
            link = "https://cdn.discordapp.com/embed/avatars/4.png"
        else:
            raise TypeError("Impossible")
        emojis = self.bot.get_guild(846318304289488906).emojis
        embed=discord.Embed(title=f"{get(emojis, name='avatar')} Default avatar color", color=colorh)
        embed.set_thumbnail(url=link)
        embed.add_field(name=f"{pronoun} a {color}-colored default avatar!", value="[Want to know how this works?](http://gg.gg/nv7ek)", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['roll','random'])
    async def dice(self, ctx, sides: int = 6, quantity: int = 1):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if sides < 1 or quantity < 1:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Argument(s) Out Of Range", description="Neither arguments can be smaller than 1!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        numbers = [random.randint(1, sides) for _ in range(0, quantity)]
        results = ""
        for num in numbers:
            results += str(num) + ", "
        embed = discord.Embed(title=f"{get(emojis, name='dice')} Dice Roll Results", description=f"You rolled `{results[:-2]}`!", color=0x36393f) if quantity == 1 else discord.Embed(title=f"{get(emojis, name='dice')} Dice Roll Results", description=f"You rolled these values: ```\n{results[:-2]}\n```That leads to a total of **{str(sum(numbers))}**!", color=0x36393f)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def coin(self, ctx, bet: str = None):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if bet and bet not in ["heads", "tails"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only bet for a `heads` or `tails`!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        result = random.choice(["heads", "tails"])
        res = f"You flipped a {result}!"
        if bet:
            res += f"\nYou won, since you bet for {bet}." if bet == result else f"\nYou lost, since you bet for {bet}."
        embed=discord.Embed(title=f"{get(emojis, name='coin')} Coin Flip Results", description=res, color=0x36393f)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(get(emojis, name='hno3'))
        payload = await self.bot.wait_for('raw_reaction_add', check=lambda payload: payload.message_id == msg.id and payload.user_id == ctx.author.id)
        if payload.emoji.name == "hno3":
            res = "Oops! You dropped your coin in a beaker of concentrated nitric acid placed conveniently nearby. The coin corroded. Better luck next time."
            res += " You lose." if bet else ""
            embed=discord.Embed(title=f"{get(emojis, name='hno3')} Something happened!", description=res, color=0x36393f)
            await msg.edit(embed=embed)
        
    ### SLASH COMMANDS ZONE ###
    
    guildID = 793495102566957096
    
    @cog_ext.cog_slash(name="da",
                       description="Returns the color of a user's default avatar",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="user",
                               description="The user to get the default avatar color from",
                               option_type=6,
                               required=False
                           )
                       ])
    async def _da(self, ctx: SlashContext, user=None):
        if user:
            remainder = int(user.discriminator) % 5
            pronoun = f"{user.name} has"
        else:
            remainder = int(ctx.author.discriminator) % 5 
            pronoun = "You have"
        if remainder == 0:
            color = "blurple"
            colorh = 0x7289DA
            link = "https://cdn.discordapp.com/embed/avatars/0.png"
        elif remainder == 1:
            color = "gray"
            colorh = 0x747F8D
            link = "https://cdn.discordapp.com/embed/avatars/1.png"
        elif remainder == 2:
            color = "green"
            colorh = 0x43B581
            link = "https://cdn.discordapp.com/embed/avatars/2.png"
        elif remainder == 3:
            color = "yellow"
            colorh = 0xFAA61A
            link = "https://cdn.discordapp.com/embed/avatars/3.png"
        elif remainder == 4:
            color = "red"
            colorh = 0xF04747
            link = "https://cdn.discordapp.com/embed/avatars/4.png"
        else:
            raise TypeError("Impossible")
        emojis = self.bot.get_guild(846318304289488906).emojis
        embed=discord.Embed(title=f"{get(emojis, name='avatar')} Default avatar color", color=colorh)
        embed.set_thumbnail(url=link)
        embed.add_field(name=f"{pronoun} a {color}-colored default avatar!", value="[Want to know how this works?](http://gg.gg/nv7ek)", inline=False)
        await ctx.send(embed=embed)
        
    @cog_ext.cog_slash(name="dice",
                       description="Rolls a number of fair dice with a number of sides each",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="sides",
                               description="The number of sides the dice has",
                               option_type=4,
                               required=False
                           ),
                           create_option(
                               name="quantity",
                               description="The number of dice to roll",
                               option_type=4,
                               required=False
                           )
                       ])
    async def _dice(self, ctx, sides: int = 6, quantity: int = 1):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if sides < 1 or quantity < 1:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Argument(s) Out Of Range", description="Neither arguments can be smaller than 1!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        numbers = [random.randint(1, sides) for _ in range(0, quantity)]
        results = ""
        for num in numbers:
            results += str(num) + ", "
        embed = discord.Embed(title=f"{get(emojis, name='dice')} Dice Roll Results", description=f"You rolled **`{results[:-2]}`**!", color=0x36393f) if quantity == 1 else discord.Embed(title=f"{get(emojis, name='dice')} Dice Roll Results", description=f"You rolled these values: ```\n{results[:-2]}\n```That leads to a total of **{str(sum(numbers))}**!", color=0x36393f)
        await ctx.send(embed=embed)
        
    @cog_ext.cog_slash(name="coin",
                       description="Flip a coin; bet for heads or tails",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="bet",
                               description="What to bet",
                               option_type=3,
                               required=False,
                               choices=[
                                   create_choice(
                                       name="heads",
                                       value="heads"
                                   ),
                                   create_choice(
                                       name="tails",
                                       value="tails"
                                   )
                               ]
                           )
                       ])
    async def _coin(self, ctx, bet: str = None):
        emojis = self.bot.get_guild(846318304289488906).emojis
        if bet and bet not in ["heads", "tails"]:
            embed = discord.Embed(title=f"{get(emojis, name='error')} Error: Invalid Argument", description="You can only bet for a `heads` or `tails`!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        result = random.choice(["heads", "tails"])
        res = f"You flipped a {result}!"
        if bet:
            res += f"\nYou won, since you bet for {bet}." if bet == result else f"\nYou lost, since you bet for {bet}."
        embed=discord.Embed(title=f"{get(emojis, name='coin')} Coin Flip Results", description=res, color=0x36393f)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(get(emojis, name='hno3'))
        payload = await self.bot.wait_for('raw_reaction_add', check=lambda payload: payload.message_id == msg.id and payload.user_id == ctx.author.id)
        if payload.emoji.name == "hno3":
            res = "Oops! You dropped your coin in a beaker of concentrated nitric acid placed conveniently nearby. The coin corroded. Better luck next time."
            res += " You lose." if bet else ""
            embed=discord.Embed(title=f"{get(emojis, name='hno3')} Something happened!", description=res, color=0x36393f)
            await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))

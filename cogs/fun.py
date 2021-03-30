import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

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
        embed=discord.Embed(title="Default avatar color", color=colorh)
        embed.set_thumbnail(url=link)
        embed.add_field(name=f"{pronoun} a {color}-colored default avatar!", value="[Want to know how this works?](http://gg.gg/nv7ek)", inline=False)
        await ctx.send(embed=embed)
        
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
    async def _da(self, ctx: SlashContext, user):
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
        embed=discord.Embed(title="Default avatar color", color=colorh)
        embed.set_thumbnail(url=link)
        embed.add_field(name=f"{pronoun} a {color}-colored default avatar!", value="[Want to know how this works?](http://gg.gg/nv7ek)", inline=False)
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Fun(bot))

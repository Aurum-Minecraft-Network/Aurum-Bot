import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from disputils import BotEmbedPaginator
import datetime


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Shows helps menu"""
        emojis = self.bot.get_guild(846318304289488906).emojis
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        if get_design()[str(ctx.author.id)]:
            title = (
                f"{get(emojis, name='help')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Aurum Bot User Guide"
            embed1 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="ping")} `a!ping`
<:space:846393726586191923> Returns the latency in ms.

{get(emojis, name="interview")} `a!interview`
<:space:846393726586191923> Initiate the Interview Wizard.

{get(emojis, name="usernamereg")} `a!usernamereg [java|bedrock] [username]`
<:space:846393726586191923> Register your Minecraft username.

{get(emojis, name="usernamequery")} `a!username [java|bedrock] [user]`
<:space:846393726586191923> Query a Minecraft username of a Discord user.""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )

            embed2 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="leaderboard")} `a!bumpleader`
<:space:846393726586191923> Gives a leaderboard of bumps.

{get(emojis, name="leaderboard")} `a!invleader`
<:space:846393726586191923> Gives a leaderboard of invites.

{get(emojis, name="bump")} `!d bump`
<:space:846393726586191923> Bumps the server on DISBOARD.

{get(emojis, name="imgur")} `a!imgur`
<:space:846393726586191923> Attach images and the bot will upload them to Imgur.

{get(emojis, name="aesthetics")} `a!customize design [simple|detailed]`
<:space:846393726586191923> Customize the design language of the bot.

{get(emojis, name="aesthetics")} `a!customize embedColor [dark|light|orange|hex]`
<:space:846393726586191923> Customize the embed sidebar color of the bot. Can be `dark` to match the Discord dark theme, `light` for light theme, `orange` to match the bot's color theme, or a custom color hex code (e.g. `ff0000`).""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )

            embed3 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="aesthetics")} `a!customize icons [true|false]`
<:space:846393726586191923> Decide whether icons show up in the bot's messages.

{get(emojis, name="source")} `a!source`
<:space:846393726586191923> Returns the source code of the bot.

{get(emojis, name="avatar")} `a!da`
<:space:846393726586191923> Returns the color of a user's default avatar.

{get(emojis, name="dice")} `a!dice {{sides}} {{quantity}}`
<:space:846393726586191923> Rolls a number of fair dice with a number of sides each.

{get(emojis, name="coin")} `a!coin {{bet}}`
<:space:846393726586191923> Flip a coin; bet for heads or tails. Something might also happen...

{get(emojis, name="card")} `a!rank {{mentionuser}}`
<:space:846393726586191923> Returns a rank card of yours, or a specified user.""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )

            embed4 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="faq")} `a!faq {{entry}}`
<:space:846393726586191923> Returns a list of frequently asked questions.

{get(emojis, name="lightmode")} `a!updateRankTheme [dark|light]`
<:space:846393726586191923> Changes the theme of rank cards for you.

{get(emojis, name="leaderboard")} `a!levels`
<:space:846393726586191923> Returns a leaderboard of levels.

{get(emojis, name="help")} `a!help`
<:space:846393726586191923> This command.""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed1.set_footer(text="[] Required {} Optional")
            embed2.set_footer(text="[] Required {} Optional")
            embed3.set_footer(text="[] Required {} Optional")
            embed4.set_footer(text="[] Required {} Optional")
            embeds = [embed1, embed2, embed3, embed4]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        else:
            title = (
                f"{get(emojis, name='help')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Aurum Bot User Guide"
            embed1 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed2 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed3 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed4 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed1.add_field(
                name="a!ping", value="Returns the latency in ms.", inline=False
            )
            embed1.add_field(
                name="a!interview", value="Initiate the Interview Wizard.", inline=False
            )
            embed1.add_field(
                name="a!usernamereg [java|bedrock] [username]",
                value="Register your Minecraft username.",
                inline=False,
            )
            embed1.add_field(
                name="a!username [java|bedrock] [user]",
                value="Query a Minecraft username of a Discord user.",
                inline=False,
            )
            embed2.add_field(
                name="a!bumpleader", value="Gives a leaderboard of bumps.", inline=False
            )
            embed2.add_field(
                name="a!invleader",
                value="Gives a leaderboard of invites.",
                inline=False,
            )
            embed2.add_field(
                name="!d bump", value="Bumps the server on DISBOARD.", inline=False
            )
            embed2.add_field(
                name="a!customize design [simple|detailed]",
                value="Customize the design language of the bot.",
                inline=False,
            )
            embed2.add_field(
                name="a!customize embedColor [dark|light|orange|hex]",
                value="Customize the embed sidebar color of the bot. Can be `dark` to match the Discord dark theme, `light` for light theme, `orange` to match the bot's color theme, or a custom color hex code (e.g. `ff0000`).",
                inline=False,
            )
            embed3.add_field(
                name="a!customize icons [true|false]",
                value="Decide whether icons show up in the bot's messages.",
                inline=False,
            )
            embed3.add_field(
                name="a!imgur",
                value="Attach images and the bot will upload them to Imgur.",
                inline=False,
            )
            embed3.add_field(
                name="a!source",
                value="Returns the source code of the bot.",
                inline=False,
            )
            embed3.add_field(
                name="a!da",
                value="Returns the color of a user's default avatar.",
                inline=False,
            )
            embed3.add_field(
                name="a!dice {sides} {quantity}",
                value="Rolls a number of fair dice with a number of sides each.",
                inline=False,
            )
            embed3.add_field(
                name="a!coin {bet}",
                value="Flip a coin; bet for heads or tails. Something might also happen...",
                inline=False,
            )
            embed3.add_field(
                name="a!rank {user}",
                value="Returns a rank card of yours, or a specified user.",
                inline=False,
            )
            embed4.add_field(
                name="a!faq {entry}",
                value="Returns a list of frequently asked questions.",
                inline=False,
            )
            embed4.add_field(
                name="a!updateRankTheme [dark|light]",
                value="Changes the theme of rank cards for you.",
                inline=False,
            )
            embed4.add_field(
                name="a!levels", value="Returns a leaderboard of levels.", inline=False
            )
            embed4.add_field(name="a!help", value="This command.", inline=False)
            embed1.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed2.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed3.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed4.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed1.timestamp = datetime.datetime.utcnow()
            embed1.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed1.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embed2.timestamp = datetime.datetime.utcnow()
            embed2.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed2.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embed3.timestamp = datetime.datetime.utcnow()
            embed3.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed3.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embed4.timestamp = datetime.datetime.utcnow()
            embed4.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed4.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embeds = [embed1, embed2, embed3, embed4]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

    ### SLASH COMMANDS ZONE ###

    guildID = 793495102566957096

    @cog_ext.cog_slash(
        name="help",
        description="Returns the user guide of this self.bot",
        guild_ids=[guildID],
    )
    async def _help(self, ctx: SlashContext):
        """Shows helps menu"""
        from cogs.aesthetics import get_design, get_embedColor, get_icons

        emojis = self.bot.get_guild(846318304289488906).emojis
        if get_design()[str(ctx.author.id)]:
            title = (
                f"{get(emojis, name='help')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Aurum Bot User Guide"
            embed1 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="ping")} `/ping`
<:space:846393726586191923> Returns the latency in ms.

{get(emojis, name="usernamereg")} `/usernamereg [java|bedrock] [username]`
<:space:846393726586191923> Register your Minecraft username.

{get(emojis, name="usernamequery")} `/username [java|bedrock] [mentionuser]`
<:space:846393726586191923> Query a Minecraft username of a Discord user.""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )

            embed2 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="leaderboard")} `/bumpleader`
<:space:846393726586191923> Gives a leaderboard of bumps.

{get(emojis, name="leaderboard")} `/invleader`
<:space:846393726586191923> Gives a leaderboard of invites.

{get(emojis, name="source")} `/source`
<:space:846393726586191923> Returns the source code of the bot.

{get(emojis, name="avatar")} `/da`
<:space:846393726586191923> Returns the color of a user's default avatar.

{get(emojis, name="dice")} `/dice {{sides}} {{quantity}}`
<:space:846393726586191923> Rolls a number of fair dice with a number of sides each.

{get(emojis, name="coin")} `/coin {{bet}}`
<:space:846393726586191923> Flip a coin; bet for heads or tails. Something might also happen...""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )

            embed3 = discord.Embed(
                title=title,
                description=f"""{get(emojis, name="faq")} `/faq {{entry}}`
<:space:846393726586191923> Returns a list of frequently asked questions.

{get(emojis, name="card")} `/rank {{mentionuser}}`
<:space:846393726586191923> Returns a rank card of yours, or a specified user.

{get(emojis, name="lightmode")} `/updateRankTheme [dark|light]`
<:space:846393726586191923> Changes the theme of rank cards for you.

{get(emojis, name="leaderboard")} `/levels`
<:space:846393726586191923> Returns a leaderboard of levels.

{get(emojis, name="help")} `/help`
<:space:846393726586191923> This command.""",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed1.set_footer(text="[] Required {} Optional")
            embed2.set_footer(text="[] Required {} Optional")
            embed3.set_footer(text="[] Required {} Optional")
            embeds = [embed1, embed2, embed3]
        else:
            title = (
                f"{get(emojis, name='help')} "
                if get_icons()[str(ctx.author.id)]
                else ""
            )
            title += "Aurum Bot User Guide"
            embed1 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed2 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed3 = discord.Embed(
                title=title,
                description="Aurum Bot is the companion bot for the Aurum Minecraft Network Discord Server. Use it to play games, register usernames, apply for positions, and more. The following is a list of commands.",
                color=int(get_embedColor()[str(ctx.author.id)], 16),
            )
            embed1.add_field(
                name="/ping", value="Returns the latency in ms.", inline=False
            )
            embed1.add_field(
                name="/usernamereg [version] [username]",
                value="Register your Minecraft username.",
                inline=False,
            )
            embed1.add_field(
                name="/username [version] [user]",
                value="Query a Minecraft username of a Discord user.",
                inline=False,
            )
            embed2.add_field(
                name="/bumpleader", value="Gives a leaderboard of bumps.", inline=False
            )
            embed2.add_field(
                name="/invleader", value="Gives a leaderboard of invites.", inline=False
            )
            embed2.add_field(
                name="/source",
                value="Returns the source code of the bot.",
                inline=False,
            )
            embed2.add_field(
                name="/da",
                value="Returns the color of a user's default avatar.",
                inline=False,
            )
            embed2.add_field(
                name="/dice {sides} {quantity}",
                value="Rolls a number of fair dice with a number of sides each.",
                inline=False,
            )
            embed2.add_field(
                name="/coin {bet}",
                value="Flip a coin; bet for heads or tails. Something might also happen...",
                inline=False,
            )
            embed3.add_field(
                name="/rank {user}",
                value="Returns a rank card of yours, or a specified user.",
                inline=False,
            )
            embed3.add_field(
                name="/faq {entry}",
                value="Returns a list of frequently asked questions.",
                inline=False,
            )
            embed3.add_field(
                name="/updateRankTheme [dark|light]",
                value="Changes the theme of rank cards for you.",
                inline=False,
            )
            embed3.add_field(
                name="/levels", value="Returns a leaderboard of levels.", inline=False
            )
            embed3.add_field(name="/help", value="This command.", inline=False)
            embed1.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed2.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed3.set_thumbnail(url="https://i.imgur.com/sePqvZX.png")
            embed1.timestamp = datetime.datetime.utcnow()
            embed1.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed1.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embed2.timestamp = datetime.datetime.utcnow()
            embed2.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed2.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embed3.timestamp = datetime.datetime.utcnow()
            embed3.set_author(
                name=f"{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            embed3.set_footer(
                text="[] Required {} Optional | Aurum Bot",
                icon_url="https://i.imgur.com/sePqvZX.png",
            )
            embeds = [embed1, embed2, embed3]
        paginator = BotEmbedPaginator(ctx, embeds)
        title = (
            f"{get(emojis, name='error')} " if get_icons()[str(ctx.author.id)] else ""
        )
        title += "Refer below!"
        embed = discord.Embed(
            title=title,
            description="Refer to the message below for the help menu.",
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
        await paginator.run()


def setup(bot):
    bot.add_cog(Help(bot))

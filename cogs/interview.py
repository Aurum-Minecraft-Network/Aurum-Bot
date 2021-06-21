import discord
from discord.ext import commands
from discord.utils import get
from captcha.image import ImageCaptcha
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
        while True:
            await newInt.send(
                "Before we begin, please complete this captcha to proceed..."
            )
            captchaString = "".join(
                (
                    random.choices(
                        (
                            string.ascii_lowercase
                            + string.ascii_uppercase
                            + string.digits
                        )
                        .replace("v", "")
                        .replace("o", "")
                        .replace("u", "")
                        .replace("w", "")
                        .replace("x", "")
                        .replace("z", "")
                        .replace("c", "")
                        .replace("l", "")
                        .replace("s", ""),
                        k=random.randint(4, 6),
                    )
                )
            )  # Generate random captcha string
            image = ImageCaptcha(fonts=["assets/fonts/arial.ttf"])
            image.write(captchaString, f"captcha-{intID}.png", format="png")
            await newInt.send(file=discord.File(f"captcha-{intID}.png"))
            await newInt.send(
                """Use `a!newCaptcha` to generate a new captcha. The lowercase letters `v`, `o`, `u`, `w`, `x`, `z`, `c`, `s`, and `l` do not appear."""
            )
            print(captchaString)
            os.remove(f"captcha-{intID}.png")
            while True:
                message = await self.bot.wait_for("message")
                if message.author == ctx.author and message.channel == newInt:
                    if message.content == captchaString:
                        a = 0
                        break
                    elif message.content == "a!newCaptcha":
                        a = 1
                        break
                else:
                    continue
            if a == 1:
                continue
            elif a == 0:
                break
        await newInt.send("Captcha check completed.")
        await newInt.send(
            "Please note that all messages sent in this channel will be logged for future reference."
        )
        msg = await newInt.send(
            f"""If you agree, please choose from the following list by reacting to the message:
                           
**APPLY FOR:**
{self.ri("h")} Helper
{self.ri("e")} Developer
{self.ri("g")} Graphic Designer
{self.ri("d")} Discord Moderator
{self.ri("m")} Minecraft Moderator
{self.ri("a")} Discord + Minecraft Moderator
{self.ri("b")} City Builder

:no_entry: **__DO NOT REACT YET__**"""
        )
        await msg.add_reaction("🇭")
        await msg.add_reaction("🇪")
        await msg.add_reaction("🇬")
        await msg.add_reaction("🇩")
        await msg.add_reaction("🇲")
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        await msg.edit(
            content=f"""If you agree, please choose from the following list by reacting to the message:
                           
**APPLY FOR:**
{self.ri("h")} Helper
{self.ri("e")} Developer
{self.ri("g")} Graphic Designer
{self.ri("d")} Discord Moderator
{self.ri("m")} Minecraft Moderator
{self.ri("a")} Discord + Minecraft Moderator
{self.ri("b")} City Builder

:white_check_mark: **__REACT NOW__**"""
        )
        payload = await self.bot.wait_for(
            "raw_reaction_add",
            check=lambda payload: payload.message_id == msg.id
            and payload.user_id == ctx.author.id,
        )
        pass
        if payload.emoji.name == "🇭":
            await newInt.send("Thank you for applying for Helper!")
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
                "What time zone are you situated in? Please answer *in the form of **UTC** offset*, e.g. UTC+8, UTC+3:30"
            )
            await wait_until_done()
            await newInt.send(
                "What is the Java Edition **IP** of the Aurum Minecraft Network Main/ Parkour Server?\n\nA. bedrock.atpcity.ga\nB. java.atpcity.ga\nC. be.atpcity.ga\nD. parkour.atpcity.ga"
            )
            await wait_until_done()
            await newInt.send(
                "What is the command to go to the hub in the Main Server?"
            )
            await wait_until_done()
            await newInt.send(
                "If a player from Bedrock Edition joins the Main Server, which symbol will be prepended before their username?\n\nA. Asterisk *\nB. Dollar symbol $\nC. Hashtag #\nD. Ampersand &"
            )
            await wait_until_done()
            await newInt.send(
                """Situation: a player with the username `JebPlayz` needs help, and approaches you. Assume that you are a helper in Aurum Minecraft Network, and your username is `BobbyPlayz`."""
            )
            await newInt.send(
                '1. He has got the "Unable to connect to world." issue. What would you do to help him troubleshoot?'
            )
            await wait_until_done()
            await newInt.send(
                """2. He wants to teleport to you. What command would you use to teleport him to you?\n***DO NOT*** use any entity selectors (`@s` `@e` `@a` `@r` `@p`)."""
            )
            await wait_until_done()
            await newInt.send(
                "3. He got a broken pipe issue. You suggest him to open a ticket to get the issue solved. Which Discord channel shall he go to open a ticket? Mention the channel."
            )
            await wait_until_done()
            await newInt.send(
                "Why do you want to become a helper? Please briefly explain."
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
            await newInt.set_permissions(
                get(guild.roles, id=EVERYBODY_ROLE_ID), overwrite=perms
            )
            await newInt.edit(
                category=get(guild.channels, id=817798276366991371),
                name=f"int-ar-{intID}",
            )
        elif payload.emoji.name == "🇩":
            await newInt.send("Thank you for applying for Discord Moderator!")
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
                "Please briefly explain why would you like to become a Discord Moderator."
            )
            await wait_until_done()
            await newInt.send(
                "What would you do for the server, if you successfully become a Discord Moderator?"
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
        elif payload.emoji.name == "🇲":
            await newInt.send("Thank you for applying for Minecraft Moderator!")
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
                "Please briefly explain why would you like to become a Minecraft Moderator."
            )
            await wait_until_done()
            await newInt.send(
                "What would you do for the server, if you successfully become a Minecraft Moderator?"
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
        elif payload.emoji.name == "🇦":
            await newInt.send(
                "Thank you for applying for Discord + Minecraft Moderator!"
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
                "Please briefly explain why would you like to become a Discord + Minecraft Moderator."
            )
            await wait_until_done()
            await newInt.send(
                "What would you do for the server, if you successfully become a Discord + Minecraft Moderator?"
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
        elif payload.emoji.name == "🇪":
            await newInt.send("Thank you for applying for Developer!")
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
            await newInt.send(
                "Although we would very love to have you on board already, it is necessary for us to prove that you have some programming abilities. Therefore, all applicants must solve a programming problem to proceed."
            )
            await newInt.send(
                """Create a function called `fizz` that takes in five arguments:
    An integer called `num1`, and a string called `str1`, which defines that the multiple of `num1` has to been replaced by `str1`.
    An integer called `num2`, and a string called `str2`, which defines that the multiple of `num2` has to been replaced by `str2`.
    A list/ an array called `range`, which defines the upper and lower bound of numbers to be iterated in.
Use any programming language."""
            )
            await newInt.send(
                """Example input in Python:```py
fizz(3, \"Fizz\", 5, \"Buzz\", range(1, 16))```Console output:```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz```

Example input in JavaScript ES6:```js
range = [...Array(10).keys()];
fizz(2, "ATP", 3, "City", range);```Console output:```
0
1
ATP
City
ATP
5
ATPCity
7
ATP
City```"""
            )
            await newInt.send(
                """Python starter code ```py
def fizz(num1: int, str1: str, num2: int, str2: str, range: list):
    pass # Put your code here

fizz(
    # Parameters here
)```"""
            )
            await newInt.send(
                """JavaScript starter code ```js
function fizz(num1, str1, num2, str2, range) {
    // Put your code here
}

fizz(
    // Parameters here
);```"""
            )
            await newInt.send(
                """Java starter code ```java
public class Main {
    static void fizz(int num1, String str1, int num2, String str2, int[] range) {
        // Put your code here
    }
    
    public static void main(String[] args) {
        fizz(
            // Parameters here
        );
    }
}```"""
            )
            await newInt.send(
                """C++ starter code ```cpp
#include <iostream>
#include <string>
using namespace std;

void fizz(int num1, string str1, int num2, string str2, int[] range) {
    // Put your code here
}

int main() {
    fizz(
        // Parameters here
    );
}```"""
            )
            await newInt.send(
                "When you are done, send the code in a formatted way.\nMore info: https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51#syntax-highlighting"
            )
            await wait_until_done()
            await newInt.send("Now, please tell us your Minecraft username.")
            await wait_until_done()
            await newInt.send(
                "Please briefly explain why would you want to become a developer and help us."
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


def setup(bot):
    bot.add_cog(Interview(bot))

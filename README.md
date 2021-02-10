# ATP City Bot
This is the bot for use in the [ATP City Discord Server](https://discord.atpcity.ga).

## Runtime
This bot is run using the [PyPy interpreter](https://www.pypy.org/) to improve performance, but any interpreter should work.

## Environmental Variables
To run the bot, a few environmental variables have to be initialized. Most likely you have to create a file called `.env` at the root of this project.
An `.env` file should look like this: 

    TOKEN = yourTokenHere
    OWNER = yourDiscordUserIDHere
    ID = yourBotClientIDHere
    AWSKEY = yourAWSAccessKeyIDHere
    AWSSECRET = yourAWSSecretAccessKeyHere

Put your Discord Bot token (obtain one [here](https://www.writebots.com/discord-bot-token/)) in place of `yourTokenHere`.
Put your own Discord user ID in place of `yourDiscordUserIDHere`.
Put your Discord Bot's Client ID in place of `yourBotClientIDHere`.
Put your AWS S3 Bucket's Access Key in place of `yourAWSAccessKeyIDHere`.
Put your AWS Secret Access Key in place of `yourAWSSecretAccessKeyHere`.

## Install dependencies
Dependencies are listed in the `requirements.txt` file. Install them using pip with `pip install -r requirements.txt`.

## To run
Run the `main.py` file in any way you wish.

## Features
- A [DISBOARD](https://disboard.org) bump reminder
- A system to generate mnemonic codes based on a user's unique Discord User ID (insecure!)
- An FAQ command
- Several fun commands including a command that gets the color of a user's default avatar
- Invite Manager module that tries to figure out who invited a new joined user, and what link did the new user use to join a server (unreliable)
- Commands to register Minecraft Bedrock and Java usernames to a JSON file `usernames.json` and to query any Discord user's Minecraft usernames.
- Command which forward messages (player join/ leave events, chat messages) from [MCPEDiscordRelay](https://github.com/nomadjimbob/MCPEDiscordRelay) to another channel, allowing you to log both the console and player events on Discord, without letting normal users see what they shouldn't.

## Compatibility
Most of the features are designed with only the ATP City Discord Server in mind, and are server-specific.
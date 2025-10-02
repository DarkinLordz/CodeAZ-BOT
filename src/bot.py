from path import CONFIG_FILE, LOG_FILE
from discord.ext import commands
import discord
import json

"""
When contributing, try to keep most of the code inside bot.py
In the next patch, I will add reaction roles and improve code readabilty.
"""

# Basic logging function
def log(error):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(error)

# Load configuration
with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

discord_token = config.get("DISCORD_TOKEN")  # Bot token
command_prefix = config.get("COMMAND_PREFIX")  # Command prefix
if config.get("ALLOWED_CHANNEL?"):  # Limit bot to one channel if True
    allowed_channel_id = config.get("ALLOWED_CHANNEL_ID")
if config.get("WELCOME_MESSAGE?"):  # Enable welcome messages if True
    welcome_channel_id = config.get("WELCOME_CHANNEL_ID")
    welcome_message = config.get("WELCOME_MESSAGE")

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for on_member_join

# Create bot
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# Limit commands to allowed channel - This feature is complete
if config.get("ALLOWED_CHANNEL?") == True:
    try:
        @bot.check
        async def globally_check_channel(ctx):
            return ctx.channel.id == allowed_channel_id
    except Exception as error:
        log(error)

# Welcome new members - This feature is complete
if config.get("WELCOME_MESSAGE?") == True:
    try:
        @bot.event
        async def on_member_join(member):
            channel = bot.get_channel(welcome_channel_id)
            await channel.send(f"{welcome_message}, {member.mention} 🎉")
    except Exception as error:
        log(error)

bot.run(discord_token)
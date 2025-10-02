from discord.ext import commands
from path import CONFIG_FILE
import discord
import aternos
import log
import json

# Load configuration
with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

discord_token = config.get("DISCORD_TOKEN")  # Bot token
command_prefix = config.get("COMMAND_PREFIX")  # Command prefix

if config.get("CHANNEL?"): # Limit bot to one channel if True
    channel_id = config.get("CHANNEL_ID")

if config.get("WELCOME_MESSAGE?"):  # Enable welcome messages if True
    welcome_channel_id = config.get("WELCOME_CHANNEL_ID")
    welcome_message = config.get("WELCOME_MESSAGE")

if config.get("ATERNOS?"):
    aternos_username = config.get("ATERNOS_USERNAME")
    aternos_password = config.get("ATERNOS_PASSWORD")

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for on_member_join

# Create bot
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# Limit commands to allowed channel - This feature is complete
if config.get("CHANNEL?"):
    @bot.check
    async def globally_check_channel(ctx):
        try:
            return ctx.channel.id == channel_id
        except Exception as error:
            log.log(error)
            return False

# Welcome new members - This feature is complete
if config.get("WELCOME_MESSAGE?"):
    @bot.event
    async def on_member_join(member):
        try:
            channel = bot.get_channel(welcome_channel_id)
            if channel:
                await channel.send(f"{welcome_message}, {member.mention} 🎉")
        except Exception as error:
            log.log(error)

# Start Aternos - This feature is complete
if config.get("ATERNOS?"):
    @bot.command(name="start")
    async def start(ctx):
        try:
            await ctx.reply("Starting..")
            status = aternos.start(aternos_username, aternos_password)  # returns True/False
            if status:
                await ctx.reply("Started successfully ✅")
            else:
                await ctx.reply("Failure starting server ❌")
        except Exception as error:
            log.log(error)
            await ctx.send("An error occurred while starting the server ❌")

bot.run(discord_token)
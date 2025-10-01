from path import CONFIG_FILE
from discord.ext import commands
import discord
import json

with open(CONFIG_FILE) as file:
    config = json.load(file)

discord_token = config.get("DISCORD_TOKEN")
command_prefix = config.get("COMMAND_PREFIX")
allowed_channel_id = config.get("ALLOWED_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

@bot.check
async def globally_check_channel(ctx):
    return ctx.channel.id == allowed_channel_id

@bot.command(name="start")
async def start(ctx):
    pass #WIP

bot.run(discord_token)
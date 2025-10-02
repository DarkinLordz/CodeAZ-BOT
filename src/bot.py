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
    channel_id = config.get("CHANNEL")

if config.get("WELCOME_MESSAGE?"):  # Enable welcome messages if True
    welcome_channel_id = config.get("WELCOME_CHANNEL")
    welcome_message = config.get("WELCOME_MESSAGE")

if config.get("ATERNOS?"):
    aternos_username = config.get("ATERNOS_USERNAME")
    aternos_password = config.get("ATERNOS_PASSWORD")

if config.get("REACTION_ROLE?"):
    reaction_role_channel = config.get("REACTION_ROLE_CHANNEL")
    reaction_role_message = config.get("REACTION_ROLE_MESSAGE")
    reaction_role = config.get("REACTION_ROLE")

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True # Required for reaction_roles
intents.members = True  # Required for welcome_message

# Create bot
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# --- BOT FUNCTIONS ---

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
                await ctx.reply("Failure starting ❌")
        except Exception as error:
            log.log(error)
            await ctx.send("An error occurred while starting ❌")

# Reaction Role - This feature is complete
if config.get("REACTION_ROLE?"):
    @bot.event
    async def on_raw_reaction_add(payload):
        try:
            if payload.message_id != reaction_role_message:
                return
            
            guild = bot.get_guild(payload.guild_id)
            role_id = reaction_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)
                if role and member:
                    await member.add_roles(role)
                    print(f"Added {role.name} to {member.display_name}")
        except Exception as error:
            log.log(error)

    @bot.event
    async def on_raw_reaction_remove(payload):
        try:
            if payload.message_id != reaction_role_message:
                return

            guild = bot.get_guild(payload.guild_id)
            role_id = reaction_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)
                if role and member:
                    await member.remove_roles(role)
                    print(f"Removed {role.name} from {member.display_name}")
        except Exception as error:
            log.log(error)

bot.run(discord_token)
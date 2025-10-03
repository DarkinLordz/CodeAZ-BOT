from discord.ext import commands
from path import CONFIG_FILE
import discord
import json
import log

# --- BOT CONFIGURATION ---

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

discord_token = config.get("DISCORD_TOKEN")
command_prefix = config.get("COMMAND_PREFIX")

if config.get("CHANNEL?"):
    channel_id = config.get("CHANNEL")

if config.get("WELCOME_MESSAGE?"):
    welcome_channel_id = config.get("WELCOME_CHANNEL")
    welcome_message = config.get("WELCOME_MESSAGE")

if config.get("REACTION_ROLE?"):
    reaction_role_channel = config.get("REACTION_ROLE_CHANNEL")
    reaction_role_message = config.get("REACTION_ROLE_MESSAGE")
    reaction_role = config.get("REACTION_ROLE")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents, help_command=None)

# --- BOT FUNCTIONS ---

# Limit commands to one channel - This feature is complete
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
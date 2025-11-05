from path import CONFIG_JSON, XP_JSON
from discord.ext import commands
import discord
import json

"""
Please make sure your code works properly and follows the existing style of the project before submitting a pull request.
I appreciate all contributions in advance, thank you for helping improve this project.
"""

# --- BOT CONFIGURATION ---

with open(CONFIG_JSON, "r", encoding="utf-8") as file:
    config = json.load(file)

discord_token = config.get("DISCORD_TOKEN")
command_prefix = config.get("COMMAND_PREFIX")

if config.get("CHANNEL?"):
    channel = config.get("CHANNEL")

if config.get("WELCOME_MESSAGE?"):
    welcome_channel = config.get("WELCOME_CHANNEL")
    welcome_message = config.get("WELCOME_MESSAGE")
    if config.get("WELCOME_ROLE?"):
        welcome_role = config.get("WELCOME_ROLE")

if config.get("REACTION_ROLE?"):
    reaction_role_channel = config.get("REACTION_ROLE_CHANNEL")
    reaction_role_message = config.get("REACTION_ROLE_MESSAGE")
    reaction_role = config.get("REACTION_ROLE")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents, help_command=None)

# --- BOT FUNCTION ---

# Limit commands to one channel
if config.get("CHANNEL?"):
    @bot.check
    async def globally_check_channel(ctx):
        return ctx.channel.id == channel

# Welcome new member
if config.get("WELCOME_MESSAGE?"):
    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(welcome_channel)
        if channel:
            await channel.send(f"{welcome_message}, {member.mention} 🎉")
        if config.get("WELCOME_ROLE?"):
            role = discord.utils.get(member.guild.roles, id=welcome_role)
            await member.add_roles(role)

# Reaction Role
if config.get("REACTION_ROLE?"):
    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.message_id != reaction_role_message:
            return
        
        guild = bot.get_guild(payload.guild_id)
        role_id = reaction_role.get(str(payload.emoji))
        if role_id:
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.add_roles(role)

    @bot.event
    async def on_raw_reaction_remove(payload):
        if payload.message_id != reaction_role_message:
            return

        guild = bot.get_guild(payload.guild_id)
        role_id = reaction_role.get(str(payload.emoji))
        if role_id:
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.remove_roles(role)

# XP System
if config.get("XP_SYSTEM?"):
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        with open(XP_JSON, "r", encoding="utf-8") as file:
            xp_data = json.load(file)

        user_id = str(message.author.id)
        xp_data[user_id] = xp_data.get(user_id, 0) + 1

        with open(XP_JSON, "w", encoding="utf-8") as file:
            json.dump(xp_data, file, indent=4)

        await bot.process_commands(message)

    @bot.command(name="xp")
    async def xp_leaderboard(ctx):
        with open(XP_JSON, "r", encoding="utf-8") as file:
                xp_data = json.load(file)

        top_users = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)[:10]

        leaderboard = "**🏆 XP Sıralaması 🏆**\n"
        for i, (user_id, xp) in enumerate(top_users, start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User ID {user_id}"
            leaderboard += f"{i}. {name} — {xp} XP\n"

        await ctx.send(leaderboard)

bot.run(discord_token)

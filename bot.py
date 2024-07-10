import discord
from discord.ext import commands
import asyncio

TOKEN = 'your_token_here'  # Replace 'your_token_here' with your bot's token.

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def user_has_role(ctx, *roles):
    user_roles = [role.name for role in ctx.author.roles]
    return any(role in user_roles for role in roles)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.slash_command(name="setup", description="Sets up roles for the server")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    roles_to_create = {
        "Moderator": discord.Permissions(send_messages=True, manage_messages=True, read_message_history=True),
        "Content": discord.Permissions(send_messages=True, read_message_history=True),
        "Admin": discord.Permissions(administrator=True)
    }

    for role_name, permissions in roles_to_create.items():
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            await guild.create_role(name=role_name, permissions=permissions)
            await ctx.respond(f"{role_name} role created successfully.", delete_after=5)
        else:
            await ctx.respond(f"{role_name} role already exists.", delete_after=5)


@bot.slash_command(name="clear", description="Deletes all messages in the channel")
async def clear(ctx):
    if await user_has_role(ctx, "Moderator", "Admin"):
        if ctx.channel.type == discord.ChannelType.text:
            try:
                deleted = await ctx.channel.purge(limit=None)
                await ctx.respond(f'Deleted {len(deleted)} message(s)', delete_after=5)
            except discord.Forbidden:
                await ctx.respond("I don't have permissions to delete messages.")
            except discord.HTTPException:
                await ctx.respond("Failed to delete messages.")
        else:
            await ctx.respond("This command can only be used in text channels.")
    else:
        await ctx.respond("You do not have the required role to use this command.", delete_after=5)


@bot.slash_command(name="ban", description="Bans a user from the server")
async def ban(ctx, user: discord.Member, *, reason=None):
    if await user_has_role(ctx, "Moderator", "Admin"):
        await user.ban(reason=reason)
        with open("banned_users.txt", "a") as file:
            file.write(f"{user.id}, {user.name}: {reason}\n")
        await ctx.respond(f"{user.name} has been banned for: {reason}", delete_after=5)
    else:
        await ctx.respond("You do not have the required role to use this command.", delete_after=5)


@bot.slash_command(name="unban", description="Unbans a user from the server")
async def unban(ctx, user_id: int):
    if await user_has_role(ctx, "Moderator", "Admin"):
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.respond(f"{user.name} has been unbanned.", delete_after=5)
    else:
        await ctx.respond("You do not have the required role to use this command.", delete_after=5)


@bot.slash_command(name="kick", description="Kicks a user from the server")
async def kick(ctx, user: discord.Member, *, reason=None):
    if await user_has_role(ctx, "Moderator", "Admin"):
        await user.kick(reason=reason)
        await ctx.respond(f"{user.name} has been kicked for: {reason}", delete_after=5)
    else:
        await ctx.respond("You do not have the required role to use this command.", delete_after=5)


bot.run(TOKEN)

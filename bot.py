import discord
from discord.ext import commands
import asyncio

TOKEN = 'your_token_here'  # Replace 'your_token_here' with your bot's token.

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.slash_command(name="clear", description="Deletes all messages in the channel")
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
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


bot.run(TOKEN)

@bot.slash_command(name="setup", description="Sets up roles for the server")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name="Moderator")
    if not existing_role:
        permissions = discord.Permissions(send_messages=True, manage_messages=True, read_message_history=True)
        await guild.create_role(name="Moderator", permissions=permissions)
        await ctx.respond("Moderator role created successfully.", delete_after=5)
    else:
        await ctx.respond("Moderator role already exists.", delete_after=5)
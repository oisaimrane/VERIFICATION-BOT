import discord
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables to store the message and role to verify
verification_message_id = None
verification_role_id = None

# Command to set up the verification message
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_verification(ctx, role: discord.Role, *, message_text: str):
    """
    Command to set up the verification system.
    Example: !setup_verification @Verified "React to this message to get verified!"
    """
    global verification_message_id, verification_role_id

    # Send the embed message
    embed = discord.Embed(
        title="✅ Verification Required!",
        description=message_text,
        color=discord.Color.purple()
    )
    embed.set_footer(text="React below to get verified!")
    msg = await ctx.send(embed=embed)

    # Add a reaction to the message
    await msg.add_reaction("✅")

    # Save the message and role IDs
    verification_message_id = msg.id
    verification_role_id = role.id

    await ctx.send(f"Verification message set up with role: {role.name}!")


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")


@bot.event
async def on_raw_reaction_add(payload):
    global verification_message_id, verification_role_id

    # Check if it's the verification message
    if payload.message_id == verification_message_id and str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(verification_role_id)
        member = guild.get_member(payload.user_id)

        if role and member:
            await member.add_roles(role)
            await member.send(f"🎉 You have been verified and received the '{role.name}' role in {guild.name}!")
            print(f"Added {role.name} to {member.display_name}")


@bot.event
async def on_raw_reaction_remove(payload):
    global verification_message_id, verification_role_id

    # Check if it's the verification message
    if payload.message_id == verification_message_id and str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(verification_role_id)
        member = guild.get_member(payload.user_id)

        if role and member:
            await member.remove_roles(role)
            await member.send(f"🚫 Your '{role.name}' role has been removed in {guild.name}.")
            print(f"Removed {role.name} from {member.display_name}")


# Command to clear the setup
@bot.command()
@commands.has_permissions(administrator=True)
async def clear_verification(ctx):
    """
    Clears the verification setup.
    """
    global verification_message_id, verification_role_id

    verification_message_id = None
    verification_role_id = None
   

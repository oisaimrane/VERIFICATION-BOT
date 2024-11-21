import discord 
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your message ID and role ID
MESSAGE_ID = 1309133309858549791  # Replace with the ID of the message to watch
ROLE_ID = 1309130000557019197    # Replace with the ID of the "Verified" role

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)
        member = guild.get_member(payload.user_id)

        if role and member:
            await member.add_roles(role)
            # Send a feedback message to the member and log the action with emojis
            await member.send(f"🎉 Congratulations {member.display_name}! You have been verified and received the '{role.name}' role.")
            print(f"Added {role.name} to {member.display_name} ✅")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)
        member = guild.get_member(payload.user_id)

        if role and member:
            await member.remove_roles(role)
            # Send a feedback message to the member and log the action with emojis
            await member.send(f"❌ {member.display_name}, your '{role.name}' role has been removed.")
            print(f"Removed {role.name} from {member.display_name} ❌")

# Replace 'your-bot-token' with your bot's token
bot.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord.ext import commands
import sys
import etym
from dotenv import load_dotenv
import os

description = "bot to search etymonline.com"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

sync = False
if len(sys.argv) > 1:
    if sys.argv[1] in ("-sync", "-s"):
        sync = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    if sync:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands (Guild ID: {GUILD_ID})")
    print("-----")

# @bot.command()
# @commands.has_permissions(administrator=True)
# async def sync(ctx):
#     print("syncing commands")
#     synced = await bot.tree.sync(guild=ctx.guild)
#     await ctx.send(f"syncing {len(synced)} commands to {ctx.guild}")
#     print(f"synced {len(synced)} commands to {ctx.guild}")

@bot.command()
async def findEtym(ctx, word: str):
    print(str(ctx.author) + " searched for " + word)
    results = etym.search(word)
    if len(str(results)) >= 2000:
        for short in results.strShort():
            await ctx.send(short)
    else:
        await ctx.send(str(results))

# replace ctx.author -> interaction.user, ctx.send -> interaction.response.send_message
@bot.tree.command(name="etym", guild=discord.Object(id=GUILD_ID))
async def findEtym(interaction: discord.Interaction, word: str):
    print(str(interaction.user) + " searched for " + word)
    results = etym.search(word)
    if len(str(results)) >= 2000:
        for short in results.strShort():
            await interaction.response.send_message(short)
    else:
        await interaction.response.send_message(str(results))

bot.run(DISCORD_TOKEN)
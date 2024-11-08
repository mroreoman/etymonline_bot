import sys
import os

import discord
from discord.ext import commands
import dotenv

import etym

description = "bot to search etymonline.com"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SYNC = (len(sys.argv) > 1 and sys.argv[1] == "-sync")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    if SYNC:
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

@bot.command(name="etym")
async def findEtym(ctx, word: str):
    print(str(ctx.author) + " searched for " + word)
    results = etym.search(word)
    embeds = [discord.Embed.from_dict(r) for r in results.get_results()]
    for e in embeds:
        await ctx.send(embed=e)

# replace ctx.author with interaction.user
# replace ctx.send with interaction.response.send_message
@bot.tree.command(name="etym", guild=discord.Object(id=GUILD_ID))
async def findEtym(interaction: discord.Interaction, word: str):
    print(str(interaction.user) + " searched for " + word)
    results = etym.search(word)
    embeds = [discord.Embed.from_dict(r) for r in results.get_results()]
    for e in embeds:
        await interaction.response.send_message(embed=e) #FIXME interactions only have one response

bot.run(DISCORD_TOKEN)
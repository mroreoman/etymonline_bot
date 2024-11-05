import discord
from discord.ext import commands
import main
from dotenv import load_dotenv
import os

description = "bot to search etymonline.com"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("-----")

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    print("syncing commands")
    synced = await bot.tree.sync(guild=ctx.guild)
    await ctx.send(f"syncing {len(synced)} commands to {ctx.guild}")
    print(f"synced {len(synced)} commands to {ctx.guild}")

@bot.hybrid_command()
async def etym(ctx, word):
    print(str(ctx.author) + " searched for " + word)
    await ctx.send(main.search(word))

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
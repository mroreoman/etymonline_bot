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
async def etym(ctx, word):
    await ctx.send(main.search(word))

load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))
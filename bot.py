import sys
import os
import random

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

@bot.command()
async def grr(ctx:commands.Context):
    msg = "g" + "r" * random.randint(0, 50)
    print(msg)
    await ctx.send(msg)

@bot.command()
async def test(ctx:commands.Context):
    print(str(ctx.author) + " ran test")
    embed_list = []
    msg = "hey guys its me vikkstar123 and welcome to another episode of how to minecraft season 3."
    for i in range(1, 11):
        embed_list.append(discord.Embed.from_dict({"title": f"{i}", "description": msg * i}))
    print(embed_list)
    await ctx.send(embeds=embed_list)

@bot.command(name="etym")
async def findEtym(ctx:commands.Context, word:str): #FIXME allow spaces in parameters
    print(str(ctx.author) + " searched for " + word)
    results = etym.search(word)
    embeds_ = [discord.Embed.from_dict(r) for r in results.get_results()]
    for e in embeds_:
        await ctx.send(embed=e)

# @bot.tree.command(name="etym", guild=discord.Object(id=GUILD_ID)) #FIXME disable bc not able to send multiple embeds
# async def findEtym(interaction:discord.Interaction, word:str):
#     print(str(interaction.user) + " searched for " + word)
#     results = etym.search(word)
#     embeds_ = [discord.Embed.from_dict(r) for r in results.get_results()]

#     first = True
#     for e in embeds_:
#         if first:
#             await interaction.response.send_message(embed=e)
#         else:
#             await interaction.followup.send(embed=e) #FIXME this way just doesn't do anything

#     # await interaction.response.send_message(content=str(embeds_), embeds=embeds_) #FIXME only sends first embed?

bot.run(DISCORD_TOKEN)
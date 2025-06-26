import discord
from discord.ext import commands
import os
import config
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} 온라인!")

async def load_cogs():
    for folder_name in os.listdir("cogs"):
        if not folder_name.startswith("_"):
            for file_name in os.listdir(f"cogs/{folder_name}"):
                if file_name.endswith(".py") and not file_name.startswith("_"):
                    await bot.load_extension(f"cogs.{folder_name}.{file_name[:-3]}")


async def main():
    await load_cogs()
    try:
        await bot.start(config.TOKEN)
    finally:
        await bot.close()

asyncio.run(main())
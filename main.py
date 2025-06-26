import discord
from discord.ext import commands
import os
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} 온라인!")


async def load_cogs():
    for forder_name in os.listdir("cogs"):
        if not forder_name.startswith("_"):
            for file_name in os.listdir(f"cogs/{forder_name}"):
                if file_name.endswith(".py") and not file_name.startswith("_"):
                    await bot.load_extension(f"cogs.{forder_name}.{file_name[:-3]}")


async def main():
    await load_cogs()
    await bot.start(config.TOKEN)

import asyncio
asyncio.run(main())
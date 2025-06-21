import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *


class ScheduleDeleteSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="delete_schedule", description="플랜을 삭제합니다.")
    @app_commands.describe(title="삭제할 플랜 제목")
    async def delete_schedule(self, interaction: discord.Interaction, title: str):
        plans = load_file("database", "multi.json")

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return

        del plans[title]
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"'{title}' 플랜이 삭제되었습니다.")

async def setup(bot):
    await bot.add_cog(ScheduleDeleteSlashes(bot))
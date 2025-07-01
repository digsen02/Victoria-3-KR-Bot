import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *


class ScheduleReserveSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reserve", description="플랜에 예약합니다.")
    @app_commands.describe(title="플랜 제목 (예: 2025-06-09_18:30)")
    async def reserve(self, interaction: discord.Interaction, title: str):
        plans = load_file("database", "multi.json")

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        if user_id in plans[title]["players"]:
            await interaction.response.send_message("이미 예약하셨습니다.", ephemeral=True)
            return

        plans[title]["current_players"] += 1

        plans[title]["players"].append(user_id)
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"{interaction.user.mention}님이 '{title}' 플랜에 예약되었습니다!")


async def setup(bot):
    await bot.add_cog(ScheduleReserveSlash(bot))
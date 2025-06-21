import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *


class ScheduleShowSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_schedules", description="모든 플랜을 보여줍니다.")
    async def show_schedules(self, interaction: discord.Interaction):
        plans = load_file("database", "multi.json")

        if not plans:
            await interaction.response.send_message("현재 등록된 플랜이 없습니다.")
            return

        msg = "**📅 현재 등록된 플랜 목록:**\n"
        for title, info in plans.items():
            date = info["date"]
            members = ", ".join([f"<@{uid}>" for uid in info["members"]])
            msg += f"\n**{title}** ({date})\n예약자: {members or '없음'}\n"

        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(ScheduleShowSlash(bot))
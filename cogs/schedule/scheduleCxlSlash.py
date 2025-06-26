import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *


class ScheduleCxlSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cxl", description="예약을 취소합니다.")
    @app_commands.describe(title="예약을 취소 할 플랜 제목")
    async def scheduleCxlSlash(self, interaction: discord.Interaction, title: str):
        if title not in load_file("database", "multi.json"):
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return
        if interaction.user.id not in load_file("database", "multi.json")[title]["players"]:
            await interaction.response.send_message("예약하지 않은 플랜 입니다.", ephemeral=True)
        else:
            load_file("database", "multi.json")[title]["players"].remove(interaction.user.id)
            save_file("database", "multi.json", load_file("database", "multi.json"))
            await interaction.response.send_message(f"{interaction.user.mention}님이 '{title}' 플랜에 예약을 취소했습니다!")



async def setup(bot):
    await bot.add_cog(ScheduleCxlSlash(bot))
from typing import Optional
import datetime
import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *

class ScheduleMadeSlash(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @app_commands.command(name="make_schedule", description="멀티예약")
    @app_commands.describe(
        year="연도",
        month="월",
        day="일",
        hour="시",
        minute="분",
        min_players="최소 시작 인원",
        ruleset="적용 할 룰"
    )
    async def schedule_made(
        self,
        interaction: discord.Interaction,
        ruleset: int,
        day: int,
        hour: int,
        minute: int,
        year: Optional[int] = datetime.date.today().year,
        month: Optional[int] = datetime.date.today().month,
        min_players: Optional[int] = 2
    ):
        try:
            validate_year(year)
            validate_month(month)
            validate_day(day)
            validate_hour(hour)
            validate_minute(minute)
        except ValueError as e:
            await interaction.response.send_message(f"입력 오류: {str(e)}", ephemeral=True)
            return
        await interaction.response.send_message(f"예약일시: {year}-{month}-{day} {hour}:{minute} / 룰셋: {ruleset} / 최소 인원: {min_players}")

async def setup(bot):
    await bot.add_cog(ScheduleMadeSlash(bot))
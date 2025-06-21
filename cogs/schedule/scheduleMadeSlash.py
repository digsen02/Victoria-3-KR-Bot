import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *


PLAN_FILE = os.path.join("database", "multi.json")

class ScheduleMadeSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="make_schedule", description="멀티 플랜을 생성합니다.")
    @app_commands.describe(
        year="연도 (기본값: 올해)",
        month="월",
        day="일",
        hour="시",
        minute="분",
        ruleset="룰셋 번호",
        min_players="최소 시작 인원"
    )

    # load, save 함수를 utils에 넣음

    async def make_schedule(
        self,
        interaction: discord.Interaction,
        ruleset: int,
        day: int,
        hour: int,
        minute: int,
        year: Optional[int] = datetime.datetime.today().year,
        month: Optional[int] = datetime.datetime.today().month,
        min_players: Optional[int] = 2
    ):
        print(interaction.user.id)

        try:
            validate_year(year)
            validate_month(month)
            validate_day(day)
            validate_hour(hour)
            validate_minute(minute)
        except ValueError as e:
            await interaction.response.send_message(f"입력 오류: {str(e)}", ephemeral=True)
            return
        print(interaction.user.id)

        date = datetime.datetime(year, month, day, hour, minute)
        title = f"{year}-{month:02}-{day:02}_{hour:02}:{minute:02}"
        alert_time = (date - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")

        plans = load_file("database", "multi.json")
        print(interaction.user.id)

        #++
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if alert_time < now:
            alert_time = date.strftime("%Y-%m-%d %H:%M")
        #

        if title in plans:
            await interaction.response.send_message("이미 해당 시간의 플랜이 존재합니다.", ephemeral=True)
            return

        plans[title] = {
            "date": date.strftime("%Y-%m-%d %H:%M"),
            "alert_time": alert_time,
            "members": [str(interaction.user.id)],
            "ruleset": ruleset,
            "min_players": min_players
        }
        print(interaction.user.id)

        save_file("database", "multi.json", plans)
        print(interaction.user.id)

        await interaction.response.send_message(
            f"✅ 예약일시: {year}-{month}-{day} {hour}:{minute}\n"
            f"📜 룰셋: {ruleset} / 👥 최소 인원: {min_players}\n"
            f"{interaction.user.mention}님이 예약자로 등록되었습니다!"
        )


async def setup(bot):
    await bot.add_cog(ScheduleMadeSlash(bot))
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import datetime
import os
import json

from utils.DateJudg import (
    validate_year, validate_month, validate_day,
    validate_hour, validate_minute
)

PLAN_FILE = os.path.join("database", "plans.json")

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
        try:
            validate_year(year)
            validate_month(month)
            validate_day(day)
            validate_hour(hour)
            validate_minute(minute)
        except ValueError as e:
            await interaction.response.send_message(f"입력 오류: {str(e)}", ephemeral=True)
            return

        date = datetime.datetime(year, month, day, hour, minute)
        title = f"{year}-{month:02}-{day:02}_{hour:02}:{minute:02}"

        try:
            with open(PLAN_FILE, "r", encoding="utf-8") as f:
                plans = json.load(f)
        except FileNotFoundError:
            plans = {}

        if title in plans:
            await interaction.response.send_message("이미 해당 시간의 플랜이 존재합니다.", ephemeral=True)
            return

        plans[title] = {
            "date": date.strftime("%Y-%m-%d %H:%M"),
            "members": [str(interaction.user.id)],
            "ruleset": ruleset,
            "min_players": min_players,
            "notified": False
        }

        with open(PLAN_FILE, "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)

        await interaction.response.send_message(
            f"✅ 예약일시: {year}-{month}-{day} {hour}:{minute}\n"
            f"📜 룰셋: {ruleset} / 👥 최소 인원: {min_players}\n"
            f"{interaction.user.mention}님이 예약자로 등록되었습니다!"
        )

    @app_commands.command(name="reserve", description="플랜에 예약합니다.")
    @app_commands.describe(title="플랜 제목 (예: 2025-06-09_18:30)")
    async def reserve(self, interaction: discord.Interaction, title: str):
        try:
            with open(PLAN_FILE, "r", encoding="utf-8") as f:
                plans = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("아직 생성된 플랜이 없습니다.", ephemeral=True)
            return

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        if user_id in plans[title]["members"]:
            await interaction.response.send_message("이미 예약하셨습니다.", ephemeral=True)
            return

        plans[title]["members"].append(user_id)

        with open(PLAN_FILE, "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)

        await interaction.response.send_message(f"{interaction.user.mention}님이 '{title}' 플랜에 예약되었습니다!")

    @app_commands.command(name="delete_schedule", description="플랜을 삭제합니다.")
    @app_commands.describe(title="삭제할 플랜 제목")
    async def delete_schedule(self, interaction: discord.Interaction, title: str):
        try:
            with open(PLAN_FILE, "r", encoding="utf-8") as f:
                plans = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("플랜 데이터가 없습니다.", ephemeral=True)
            return

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return

        del plans[title]

        with open(PLAN_FILE, "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)

        await interaction.response.send_message(f"'{title}' 플랜이 삭제되었습니다.")

    @app_commands.command(name="show_schedules", description="모든 플랜을 보여줍니다.")
    async def show_schedules(self, interaction: discord.Interaction):
        try:
            with open(PLAN_FILE, "r", encoding="utf-8") as f:
                plans = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("아직 생성된 플랜이 없습니다.")
            return

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
    await bot.add_cog(ScheduleMadeSlash(bot))
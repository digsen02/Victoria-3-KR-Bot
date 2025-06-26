import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import json
from utils.DateJudg import *
from utils.dataFileManager import *
from notifierTask import NotifierTask
import asyncio


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
        ruleset="룰셋",
        min_players="최소 시작 인원"
    )

    async def make_schedule(
        self,
        interaction: discord.Interaction,
        day: int,
        hour: int,
        minute: int,
        ruleset: Optional[int] = 1,
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

        plans = load_file("database", "multi.json")

        if title in plans:
            await interaction.response.send_message("이미 해당 시간의 플랜이 존재합니다.", ephemeral=True)
            return

        plans[title] = {
            "unique_key": f"{str(interaction.guild.id)}_{interaction.user.id}_{date.strftime("%Y-%m-%d_%H:%M")}",
            "guild_id": str(interaction.guild.id),
            "host_id": str(interaction.user.id),
            "start_date": date.strftime("%Y-%m-%d_%H:%M"),
            "ruleset": ruleset,
            "min_players": min_players,
            "members": [str(interaction.user.id)],
            "current_players": 1,
            "occupied_nations": [],
            "player_info" : []
        }

        save_file("database", "multi.json", plans)
        notifier = NotifierTask(self.bot)
        asyncio.create_task(notifier.notify())

        embed = discord.Embed(
            title="📅 멀티 일정 생성 완료!",
            description=f"{interaction.user.mention}님이 예약자로 등록되었습니다!",
            color=discord.Color.green()
        )
        embed.add_field(name="✅ 예약일시", value=f"{year}-{month:02}-{day:02} {hour:02}:{minute:02}", inline=False)
        embed.add_field(name="📜 룰셋", value=str(ruleset), inline=True)
        embed.add_field(name="👥 최소 인원", value=str(min_players), inline=True)
        embed.set_footer(text="Victoria3 KR Server")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ScheduleMadeSlash(bot))
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
from utils.DateJudg import *
from utils.dataFileManager import *
import datetime


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
        plan_name: str,
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

        start_date = datetime.datetime(year, month, day, hour, minute).strftime("%Y-%m-%d_%H:%M")
        title = f"{plan_name}"

        plans = load_file("database", "multi.json")
        if plans is None:
            plans = {}

        if title in plans:
            await interaction.response.send_message("이미 해당 이름의 플랜이 존재합니다.", ephemeral=True)
            return

        for plan_name, plan_data in plans.items():
            if plan_data.get("start_date") == start_date:
                await interaction.response.send_message("이미 해당 시간대에 플랜이 존재합니다.", ephemeral=True)
                return

        host_id = str(interaction.user.id)

        plans[title] = {
            "unique_key": f"{str(interaction.guild.id)}_{host_id}_{start_date}",
            "guild_id": str(interaction.guild.id),
            "host_id": host_id,
            "start_date": start_date,
            "ruleset": ruleset,
            "min_players": min_players,
            "players": [
                host_id,
            ],
            "current_players": 1,
            "occupied_nations": [],
            "player_info": []
        }

        save_file("database", "multi.json", plans)

        embed = discord.Embed(
            title="📅 멀티 일정 생성 완료!",
            description=f"{interaction.user.mention}님이 예약자로 등록되었습니다!",
            color=discord.Color.green()
        )
        embed.add_field(name="플랜 제목", value=f"{plan_name}", inline=False)
        embed.add_field(name="✅ 예약일시", value=f"{year}-{month:02}-{day:02} {hour:02}:{minute:02}", inline=False)
        embed.add_field(name="📜 룰셋", value=str(ruleset), inline=True)
        embed.add_field(name="👥 최소 인원", value=str(min_players), inline=True)
        embed.set_footer(text="Victoria3 KR Server")

        await interaction.response.send_message(embed=embed)

        notifier = self.bot.get_cog("NotifierTask")
        if notifier:
            self.bot.loop.create_task(notifier.notify(interaction))
        else:
            await interaction.followup.send("NotifierTask가 없습니다.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ScheduleMadeSlash(bot))
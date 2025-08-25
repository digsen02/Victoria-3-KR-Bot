import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
from utils.DateJudg import *
from utils.dataFileManager import *
from utils.FindNearest import *
import datetime

PLAN_FILE = os.path.join("database", "multi.json")
RULE_FILE = os.path.join("database", "ruleset.json")

class ScheduleMadeSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        plans = load_file("database", "multi.json")
        if not isinstance(plans, dict):
            plans = {}
            save_file("database", "multi.json", plans)

    def load_ruleset_names(path: str = RULE_FILE) -> list[str]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        ruleset = []
        for category_dict in data.values():
            ruleset.extend(category_dict.keys())

        return ruleset
    
    ruleset_list = load_ruleset_names()
    DEFAULT_RULESET = ruleset_list[0]

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
    @app_commands.choices(
        ruleset=[
            discord.app_commands.Choice(name=name, value=name) for name in ruleset_list
        ]
    )

    async def make_schedule(
        self,
        interaction: discord.Interaction,
        plan_name: str,
        hour: int,
        minute: int,
        day: Optional[int] = datetime.datetime.today().day,
        ruleset: Optional[str] = DEFAULT_RULESET,
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

        if not isinstance(plans, dict):
            plans = {}

        #print(f"plans: {plans}, type: {type(plans)}")

        if title in plans:
            #print(f"[경고] 플랜명 '{title}' 이미 존재함. 함수 종료")
            await interaction.response.send_message("이미 해당 이름의 플랜이 존재합니다.", ephemeral=True)
            return
        
        start_dt = datetime.datetime(year, month, day, hour, minute)
        nearest_title, nearest_date = find_nearest(plans)
        if nearest_date and start_dt < nearest_date:
            if plans[nearest_title]["player_info"]:
                await interaction.response.send_message("국가가 예약된 파일보다 가까운 날짜에 플랜을 생성할 수 없습니다.", ephemeral=True)
                return

        if start_dt < datetime.datetime.now():
            await interaction.response.send_message("현재 날짜보다 뒤에 플랜을 생성할 수 없습니다.", ephemeral=True)
            return


        for plan_name, plan_data in plans.items():
            if plan_data.get("start_date") == start_date:
                await interaction.response.send_message("이미 해당 시간대에 플랜이 존재합니다.", ephemeral=True)
                return

        host_id = str(interaction.user.id)

        plans[title] = {
            "unique_key": f"{str(interaction.guild.id)}_{host_id}_{start_date}",
            "guild_id": str(interaction.guild.id),
            "channel_id" : str(interaction.channel.id),
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

        #print(f"[저장] '{title}' 플랜 저장 시작")
        save_file("database", "multi.json", plans)
        #print(f"[저장 완료] '{title}' 플랜 저장 완료")

        updated = load_file("database", "multi.json")
        if title not in updated:
            await interaction.response.send_message("저장 중 문제가 발생했습니다. 다시 시도해주세요.", ephemeral=True)
            return
        
        role_id = 0  # 멀티 알림 id 넣기
        role_mention = f"<@&{role_id}>"

        embed = discord.Embed(
            title="📅 멀티 일정 생성 완료!",
            description=f"{role_mention} {interaction.user.mention}님이 플랜을 생성하였습니다!",
            color=discord.Color.green()
        )
        embed.add_field(name="플랜 제목", value=f"{title}", inline=False)
        embed.add_field(name="✅ 예약일시", value=f"{year}-{month:02}-{day:02} {hour:02}:{minute:02}", inline=False)
        embed.add_field(name="📜 룰셋", value=str(ruleset), inline=True)
        embed.add_field(name="👥 최소 인원", value=str(min_players), inline=True)
        embed.set_footer(text="Victoria3 KR Server")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ScheduleMadeSlash(bot))
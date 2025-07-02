import discord
from discord.ext import commands, tasks
import datetime
import os
from utils.DateJudg import *
from utils.dataFileManager import *

PLAN_FILE = os.path.join("database", "multi.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.notified_plans = set()
        self.notify.start()
        #print("[NotifierTask] notify 태스크 시작됨")

    def expt_nearest(self, plans=None):
        if plans is None:
            plans = load_file("database", "multi.json") or {}

        now = datetime.datetime.now()
        #print(f"[expt_nearest] 현재 시간: {now}")
        nearest_title = None
        nearest_alert_time = None

        for title, data in plans.items():
            #print(f"---- {title} 검사 중 ----")

            if title in self.notified_plans:
                #print(f"[{title}] 이미 알림 전송됨 → 제외")
                continue

            try:
                start_time = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d_%H:%M")
            except Exception as e:
                print(f"[{title}] 날짜 파싱 실패: {e}")
                continue

            alert_time = start_time - datetime.timedelta(minutes=10)
            #print(f"[{title}] 시작 시각: {start_time} / 알림 시각: {alert_time}")

            if alert_time <= now:
                #print(f"[{title}] 알림 시각 지남 → 제외")
                continue

            if nearest_alert_time is None or alert_time < nearest_alert_time:
                nearest_alert_time = alert_time
                nearest_title = title
                #print(f"[{title}] 가장 빠른 알림 후보로 설정됨")

        #print(f"[결과] 선택된 플랜: {nearest_title}, 알림 시간: {nearest_alert_time}")
        return nearest_alert_time, nearest_title
    @tasks.loop(seconds=30)
    async def notify(self):
        plans = load_file("database", "multi.json")
        if not plans:
            return
        alert_time, nearest_title = self.expt_nearest(plans)
        #print(f"가장 가까운 플랜: {nearest_title} / 알림시간: {alert_time}")

        if nearest_title is None:
            return

        now = datetime.datetime.now()

        time_diff = (alert_time - now).total_seconds()
        if not (-30 <= time_diff <= 30):
            return

        channel_id = int(plans[nearest_title].get("channel_id"))
        if channel_id is None:
            print(f"`{nearest_title}`에 channel_id가 없습니다.")
            return

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print(f"channel_id {channel_id}에 해당하는 채널을 찾을 수 없습니다.")
            return

        mentions = " ".join([f"<@{uid}>" for uid in plans[nearest_title].get("players", [])])
        embed = discord.Embed(
            title=f"📢 알림! `{nearest_title}` 일정이 곧 시작합니다!",
            description=mentions
        )
        await channel.send(embed=embed)
        self.notified_plans.add(nearest_title)

        print(f"{nearest_title} 알림 완료")

async def setup(bot: commands.Bot):
    await bot.add_cog(NotifierTask(bot))
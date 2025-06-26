import discord
from discord.ext import tasks, commands
import datetime
import json
import os
import asyncio
from utils.FindNearest import find_nearest


PLAN_FILE = os.path.join("database", "multi.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def notify(plans):
        nearest_title, nearest_date = find_nearest(plans)

        alert_time = nearest_date - datetime.timedelta(minutes=30)
        now = datetime.datetime.now()

        if now > alert_time:
            print(f"⛔ {nearest_title}  일정의 알림시간({alert_time})은 이미 지났습니다.")
            return

        wait_seconds = (alert_time - now).total_seconds()

        await asyncio.sleep(wait_seconds)

        mentions = " ".join([f"<@{uid}>" for uid in plans[nearest_title]["members"]])
        print(f"📢 알림! `{nearest_title}` 일정이 곧 시작합니다!")
        print(f"멘션 대상: {mentions}")
import discord
from discord.ext import tasks, commands
import datetime
import json
import os
import asyncio
from utils.FindNearest import find_nearest


PLAN_FILE = os.path.join("database", "multi.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def notify(plans, interaction: discord.Interaction):
        nearest_title, nearest_date = find_nearest(plans)

        alert_time = nearest_date - datetime.timedelta(minutes=30)
        now = datetime.datetime.now()

        if now > alert_time:
            embed = discord.Embed(title="일정의 알림시간은 이미 지났습니다.")
            await interaction.response.send_message(embed=embed)
            return

        wait_seconds = (alert_time - now).total_seconds()

        await asyncio.sleep(wait_seconds)

        mentions = " ".join([f"<@{uid}>" for uid in plans[nearest_title]["members"]])
        embed = discord.Embed(
        title=f"📢 알림! `{nearest_title}` 일정이 곧 시작합니다!", description=mentions)
        await interaction.channel.send(embed=embed)
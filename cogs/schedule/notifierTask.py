import discord
from discord.ext import commands, tasks
import datetime
import os
import asyncio
from utils.DateJudg import *
from utils.FindNearest import *


PLAN_FILE = os.path.join("database", "multi.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def notify(self, interaction: discord.Interaction):

        plans = load_file("database", "multi.json")
        nearest_title, nearest_date = find_nearest(plans)

        alert_time = nearest_date - datetime.timedelta(minutes=30)
        now = datetime.datetime.now()

        if not plans:
            return

        print(str(nearest_date))

        if now > alert_time:
            embed = discord.Embed(title="일정의 알림시간은 이미 지났습니다.")
            await interaction.channel.send(embed=embed)
            return

        wait_seconds = (alert_time - now).total_seconds()
        #print("sleep.." + str(wait_seconds))
        await asyncio.sleep(wait_seconds)

        mentions = " ".join([f"<@{uid}>" for uid in plans[nearest_title]["members"]])
        embed = discord.Embed(title=f"📢 알림! `{nearest_title}` 일정이 곧 시작합니다!", description=mentions)
        await interaction.channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(NotifierTask(bot))
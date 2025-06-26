import discord
from discord.ext import tasks, commands
import datetime
import json
import os

PLAN_FILE = os.path.join("database", "multi.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_checked_minute = None
        self.task = self.bot.loop.create_task(self.wait_until_9am())


    async def notify_check(self):
        now = datetime.datetime.now()
        current_min = now.strftime("%Y-%m-%d_%H:%M")
        print(f"테스트 {self.min_check()}")
        with open(PLAN_FILE, "r") as f:
            plans = json.load(f)
        while True:
            pass


    async def before_check(self):
        await self.bot.wait_until_ready()

    @staticmethod
    def min_check():
        with open(PLAN_FILE, "r") as f:
            plans = json.load(f)
        min_time = None
        for title, data in plans.items():
            if min_time is None:
                min_time = data["date"]
            else:
                if data["date"] < min_time:
                    min_time = data["date"]
        return min_time



async def setup(bot):
    await bot.add_cog(NotifierTask(bot))
import discord
from discord.ext import tasks, commands
import datetime
import json
import os

PLAN_FILE = os.path.join("database", "plans.json")

class NotifierTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_checked_minute = None
        self.notify_check.start()

    @tasks.loop(minutes=1)
    async def notify_check(self):
        now = datetime.datetime.now()
        current_min = now.strftime("%Y-%m-%d %H:%M")

        with open(PLAN_FILE, "r") as f:
            plans = json.load(f)

        for title, data in plans.items():
            if data.get("alert_time") == current_min:
                member_ids = data.get("members", [])
                mentions = " ".join(f"<@{uid}>" for uid in member_ids)

                for guild in self.bot.guilds:
                    for channel in guild.text_channels:
                        try:
                            await channel.send(f"📢 `{title}` 플랜이 30분 후 시작됩니다! {mentions}")
                            break
                        except:
                            continue

    @notify_check.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(NotifierTask(bot))
import discord
from discord.ext import tasks, commands
import datetime
import json
import os

PLAN_FILE = os.path.join("database", "plans.json")

class CleanerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanup.start()

    @tasks.loop(hours=24)
    async def cleanup(self):
        now = datetime.datetime.now()
        with open(PLAN_FILE, "r") as f:
            plans = json.load(f)

        removed = []
        for title, data in list(plans.items()):
            plan_time = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
            if plan_time < now:
                removed.append(title)
                del plans[title]

        if removed:
            with open(PLAN_FILE, "w") as f:
                json.dump(plans, f, indent=4)

            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    try:
                        await channel.send(f"⏰ 만료된 플랜 삭제됨: {', '.join(removed)}")
                        break
                    except:
                        continue

    @cleanup.before_loop
    async def before_cleanup(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CleanerTask(bot))
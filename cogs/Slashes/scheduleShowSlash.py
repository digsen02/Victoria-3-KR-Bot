import discord
from discord.ext import commands
from discord import app_commands, Embed
from utils.dataFileManager import *


class ScheduleShowSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_schedules", description="모든 플랜을 보여줍니다.")
    async def show_schedules(self, interaction: discord.Interaction):
        plans = load_file("database", "multi.json")

        if not plans:
            embed = Embed(title="현재 등록된 플랜이 없습니다.", color=0xff0000)
            embed.set_footer(text="'make_schedule' 명령어를 사용해 플랜을 생성할 수 있습니다.")

            await interaction.response.send_message(embed=embed)
            return
        embed = Embed(title="**📅 현재 등록된 플랜 목록:**\n", color=discord.Color.green())
        for title, info in plans.items():
            members = ", ".join([f"<@{uid}>" for uid in info["members"]])
            embed.add_field(name=f"{title}", value=
            f"{members or '없음'} \n"
            f"",
                            inline=False)

            embed.set_footer(text="Victoria3 KR Server")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ScheduleShowSlash(bot))
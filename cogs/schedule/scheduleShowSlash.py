import discord
from discord.ext import commands
from discord import app_commands, Embed, Button
from utils.dataFileManager import *
from utils.page import Page, Pages

class ScheduleShowSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_schedules", description="모든 플랜을 보여줍니다.")
    async def show_schedules(self, interaction: discord.Interaction):
        plans = load_file("database", "multi.json")
        pages = []
        if not plans:
            embed = Embed(title="현재 등록된 플랜이 없습니다.", color=0xff0000)
            embed.set_footer(text="'make_schedule' 명령어를 사용해 플랜을 생성할 수 있습니다.")

            await interaction.response.send_message(embed=embed)
            return
        for title, info in plans.items():
            start_date = info.get("start_date")
            ruleset = info.get("ruleset")
            min_players = info.get("min_players")
            members = ", ".join([f"<@{uid}>" for uid in info["players"]])
            pages.append(
                Page(
                    embed= Embed(title=f"{len(pages) + 1}번째 플랜", colour= discord.Color.green())
                    .add_field(name="플랜 제목", value=f"{title}", inline=False)
                    .add_field(name=":white_check_mark: 예약일시", value=f"{start_date}", inline=False)
                    .add_field(name=":scroll: 룰셋", value=str(ruleset), inline=False)
                    .add_field(name=":busts_in_silhouette: 최소 인원", value=str(min_players), inline=False)
                    .add_field(name="플레이어", value=f"{members or '없음'}", inline=False)
                    .set_footer(text="Victoria3 KR Server"),
                    view= Button()
                )
            )
        page_manager = Pages(*pages)
        await interaction.response.send_message(embed=page_manager.current_page.embed, view=page_manager.current_page.view)

async def setup(bot):
    await bot.add_cog(ScheduleShowSlash(bot))
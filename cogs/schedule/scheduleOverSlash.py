import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *
from utils.FindNearest import *

class ScheduleOverSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="over", description="플랜을 종료합니다.")
    async def over(self, interaction: discord.Interaction):
        plans = load_file("database", "multi.json")
        nearest_title, nearest_date = find_nearest(plans)

        if not plans:
            await interaction.response.send_message("플랜이 존재하지 않습니다.", ephemeral=True)
            return
        
        if plans[nearest_title]["player_info"]:
            for nearest_title, plan in plans.items():
                player_info_list = plan.get("player_info", [])
                for entry in player_info_list:
                    try:
                        user_id, user_name, _ = entry.split("\\", 2)
                        member = interaction.guild.get_member(int(user_id))
                        if member:
                            if member.guild_permissions.administrator:
                                continue
                            await member.edit(nick=user_name)
                    except Exception as e:
                        await interaction.response.send_message(f"`{entry}` 처리 중 오류 발생: {e}")
                        return

        del plans[nearest_title]
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"`{nearest_title}` 플랜이 종료되었습니다.")

async def setup(bot):
    await bot.add_cog(ScheduleOverSlashes(bot))
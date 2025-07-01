import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *

class ScheduleDeleteSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="delete_schedule", description="플랜을 삭제합니다.")
    @app_commands.describe(title="삭제할 플랜 제목")
    async def delete_schedule(self, interaction: discord.Interaction, title: str):
        plans = load_file("database", "multi.json")

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return
        
        if plans[title]["player_info"]:
            for title, plan in plans.items():
                player_info_list = plan.get("player_info", [])
                for entry in player_info_list:
                    try:
                        user_id, user_name, _ = entry.split("_", 2)
                        member = interaction.guild.get_member(int(user_id))
                        if member:
                            if member.guild_permissions.administrator:
                                await interaction.response.send_message(f"🔒 `{user_name}` (ID: {user_id}) 은 관리자여서 닉네임 변경이 불가능합니다.")
                                continue
                            await member.edit(nick=user_name)
                            await interaction.response.send_message(f"✅ `{user_name}` (ID: {user_id}) 닉네임 변경 완료")
                        else:
                            await interaction.response.send_message(f"⚠️ ID `{user_id}` 에 해당하는 멤버를 찾을 수 없습니다.")
                    except Exception as e:
                        await interaction.response.send_message(f"❌ `{entry}` 처리 중 오류 발생: {e}")

        del plans[title]
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"'{title}' 플랜이 삭제되었습니다.")

async def setup(bot):
    await bot.add_cog(ScheduleDeleteSlashes(bot))
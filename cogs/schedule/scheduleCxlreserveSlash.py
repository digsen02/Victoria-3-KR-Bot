import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *

class ScheduleCxlreserveSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #print("작동")

    @app_commands.command(name="cxl", description="예약을 취소합니다.")
    @app_commands.describe(title="예약 취소할 플랜 제목")
    async def delete_schedule(self, interaction: discord.Interaction, title: str):
        plans = load_file("database", "multi.json")
        user_id = str(interaction.user.id)

        if title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 없습니다.", ephemeral=True)
            return
        
        if user_id not in plans[title]["players"]:
            await interaction.response.send_message("플레이어가 해당 플랜에 가입되지 않았습니다.", ephemeral = True)

        if user_id == plans[title]["host_id"]:
            await interaction.response.send_message("호스트는 예약을 취소할 수 없습니다.", ephemeral=True)
        
        for entry in plans[title]["player_info"]:
            if entry.startswith(f"{user_id}_"):
                plans[title]["player_info"].remove(entry)
                break

        plans[title]["current_players"] -= 1

        plans[title]["players"].remove(user_id)
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"'{title}' 에서 예약이 취소되었습니다.")


async def setup(bot):
    await bot.add_cog(ScheduleCxlreserveSlashes(bot))
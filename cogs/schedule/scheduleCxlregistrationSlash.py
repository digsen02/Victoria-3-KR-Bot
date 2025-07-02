import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *
from utils.FindNearest import *

class ScheduleCxlregistrationSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cxl_reg", description="국가 예약을 취소합니다.")
    async def cxl_reg(self, interaction: discord.Interaction):
        plans = load_file("database", "multi.json")
        user_id = str(interaction.user.id)
        nearest_title, nearest_date = find_nearest(plans)

        if not plans:
            await interaction.response.send_message("플랜이 없습니다.", ephemeral=True)
            return

        if not any(e.startswith(f"{user_id}_") for e in plans[nearest_title]["player_info"]):
            await interaction.response.send_message("국가 예약이 되어있지 않습니다.", ephemeral=True)
            return

        entry = next((e for e in plans[nearest_title]["player_info"] if e.startswith(f"{user_id}_")), None)

        if entry:
            plans[nearest_title]["player_info"].remove(entry)
            user_id, user_name, country = entry.split("_", 2)

            if country in plans[nearest_title]["occupied_nations"]:
                plans[nearest_title]["occupied_nations"].remove(country)

            member = interaction.guild.get_member(int(user_id))
            if member:
                if member.guild_permissions.administrator:
                    #await interaction.response.send_message(f"⚠️ 관리자 유저는 닉네임 변경이 불가하므로 수동으로 바꿔주세요!", ephemeral=True)
                    pass
                else:
                    try:
                        await member.edit(nick=user_name)
                        #await interaction.response.send_message(f"✅ `{user_name}` 닉네임 변경 완료", ephemeral=True)
                    except discord.Forbidden:
                        #await interaction.response.send_message("닉네임을 변경할 수 있는 권한이 없습니다.", ephemeral=True)
                        print("닉네임 변경 권한이 부족합니다. 봇 권한을 확인해주세요.")

            save_file("database", "multi.json", plans)
            await interaction.followup.send(f"`{nearest_title}` 에서 국가 예약이 취소되었습니다.")

async def setup(bot):
    await bot.add_cog(ScheduleCxlregistrationSlashes(bot))
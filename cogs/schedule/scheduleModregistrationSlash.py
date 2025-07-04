import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *
from utils.FindNearest import *

class ScheduleModregistrationSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def find_english_name(self, data, korean_name: str) -> str:
        for category in data:
            for country_list in category.values():
                for eng, kor in country_list:
                    if kor == korean_name:
                        return eng
        return None

    @app_commands.command(name="mod_reg", description="국가를 변경합니다.")
    @app_commands.describe(country="예약할 국가 이름")
    async def mod_reg(self, interaction: discord.Interaction, country: str):
        plans = load_file("database", "multi.json")
        countries = load_file("database", "country.json")
        user_id = str(interaction.user.id)
        nearest_title, nearest_date = find_nearest(plans)

        if not plans:
            await interaction.response.send_message("플랜이 없습니다.", ephemeral=True)
            return
        
        if nearest_title not in plans:
            await interaction.response.send_message("해당 제목의 플랜이 존재하지 않습니다.", ephemeral=True)
            return
        
        print("존재함")
        
        if not any(e.startswith(f"{user_id}_") for e in plans[nearest_title]["player_info"]):
            await interaction.response.send_message("국가 예약이 되어있지 않습니다.", ephemeral=True)
            return
        
        print("존재함2")
        
        english_name = self.find_english_name(countries, country)
        if english_name is None:
            await interaction.response.send_message("존재하지 않는 국가입니다. 정확히 입력해주세요.", ephemeral=True)
            return
        
        print("존재함3")
        
        if english_name in plans[nearest_title]["occupied_nations"]:
            await interaction.response.send_message("이미 점유된 국가입니다.", ephemeral=True)
            return
        
        print("존재함4")

        entry = next((e for e in plans[nearest_title]["player_info"] if e.startswith(f"{user_id}_")), None)
        member = interaction.guild.get_member(interaction.user.id)
        display_name = member.display_name if member else interaction.user.name

        print("여까지 실행됨")

        if entry:
            plans[nearest_title]["player_info"].remove(entry)
            print("여까지 실행됨2-1")
            n_user_id, user_name, b_country = entry.split("_", 2)
            print("여까지 실행됨2")

            if b_country in plans[nearest_title]["occupied_nations"]:
                plans[nearest_title]["occupied_nations"].remove(b_country)
                print("여까지 실행됨 3")

            member = interaction.guild.get_member(int(n_user_id))
            if member:
                print("여까지 실행됨 4")
                player_entry = f"{n_user_id}_{user_name}_{english_name}"
                plans[nearest_title]["player_info"].append(player_entry)
                plans[nearest_title]["occupied_nations"].append(str(english_name))
        
                await interaction.response.send_message(f"국가를 `{country}`으로 변경하였습니다.")

                if member.guild_permissions.administrator:
                    #await interaction.followup.send(f"⚠️ 관리자 유저는 닉네임 변경이 불가하므로 수동으로 바꿔주세요!", ephemeral=True)
                    pass
                else:
                    try:
                        await member.edit(nick=country)
                        await interaction.followup.send(f"✅ `{user_name}` 닉네임 변경 완료", ephemeral=True)
                    except discord.Forbidden:
                        #await interaction.followup.send("닉네임을 변경할 수 있는 권한이 없습니다.", ephemeral=True)
                        print("닉네임 변경 권한이 부족합니다. 봇 권한을 확인해주세요.")

            save_file("database", "multi.json", plans)
            
async def setup(bot):
    await bot.add_cog(ScheduleModregistrationSlashes(bot))
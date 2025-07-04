import discord
from discord.ext import commands
from discord import app_commands
from utils.DateJudg import *
from utils.dataFileManager import *
from utils.FindNearest import *

class ScheduleRegistrationSlashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #print("작동")

    def find_english_name(self, data, korean_name: str) -> str:
        for category in data:
            for country_list in category.values():
                for eng, kor in country_list:
                    if kor == korean_name:
                        return eng
        return None

    @app_commands.command(name="reg", description="국가를 예약합니다.")
    @app_commands.describe(country="예약할 국가 이름")
    async def reg(self, interaction: discord.Interaction, country: str):
        #print("실행")
        plans = load_file("database", "multi.json")
        countries = load_file("database", "country.json")
        user_id = str(interaction.user.id)
        nearest_title, nearest_date = find_nearest(plans)

        plans = load_file("database", "multi.json")
        if not plans:
            await interaction.response.send_message("플랜이 비어있습니다.", ephemeral=True)
            return

        countries = load_file("database", "country.json")

        nearest_title, nearest_date = find_nearest(plans)

        user_id = str(interaction.user.id)
        if user_id not in plans[nearest_title]["players"]:
            await interaction.response.send_message("가장 가까운 플랜에 예약되어있지 않습니다.", ephemeral=True)
            return

        english_name = self.find_english_name(countries, country)
        if english_name is None:
            await interaction.response.send_message("존재하지 않는 국가입니다. 정확히 입력해주세요.", ephemeral=True)
            return
        
        if english_name in plans[nearest_title]["occupied_nations"]:
            await interaction.response.send_message("이미 점유된 국가입니다.", ephemeral=True)
            return

        member = interaction.guild.get_member(interaction.user.id)
        display_name = member.display_name if member else interaction.user.name

        for info in plans[nearest_title]["player_info"]:
            if info.startswith(f"|"):
                await interaction.response.send_message("이미 국가를 예약하셨습니다.", ephemeral=True)
                return

        player_entry = f"{user_id}|{display_name}|{english_name}"
        plans[nearest_title]["player_info"].append(player_entry)
        plans[nearest_title]["occupied_nations"].append(str(english_name))
        save_file("database", "multi.json", plans)

        await interaction.response.send_message(f"✅ {interaction.user.mention}님이 `{nearest_title}` 플랜에 `{country}` 국가로 예약되었습니다!")

        if member.guild_permissions.administrator:
            #await interaction.followup.send("⚠️ 관리자 유저는 닉네임 변경이 불가하므로 수동으로 바꿔주세요!", ephemeral=True)
            return
        try:
            await member.edit(nick=country)
        except discord.Forbidden:
            #await interaction.followup.send("닉네임 변경 권한이 부족합니다. 봇 권한을 확인해주세요.", ephemeral=True)
            print("닉네임 변경 권한이 부족합니다. 봇 권한을 확인해주세요.")

async def setup(bot):
    await bot.add_cog(ScheduleRegistrationSlashes(bot))
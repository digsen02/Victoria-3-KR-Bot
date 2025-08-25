import discord
from discord.ext import commands
from discord import app_commands, Embed
from discord.ui import View, Button
from utils.dataFileManager import load_file, save_file
from utils.page import Page

class PagesManager:
    """Pages와 Buttons 통합 관리"""
    def __init__(self, pages: list[Page]):
        self.pages = pages
        self.index = 0

    @property
    def current_page(self):
        return self.pages[self.index]

    def next_page(self):
        self.index = (self.index + 1) % len(self.pages)
        return self.current_page

    def prev_page(self):
        self.index = (self.index - 1) % len(self.pages)
        return self.current_page


class ScheduleShowSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_schedules", description="모든 플랜을 보여줍니다.")
    async def show_schedules(self, interaction: discord.Interaction):
        await interaction.response.defer()

        plans = load_file("database", "multi.json")
        if not plans:
            embed = Embed(title="현재 등록된 플랜이 없습니다.", color=0xff0000)
            embed.set_footer(text="'make_schedule' 명령어를 사용해 플랜을 생성할 수 있습니다.")
            await interaction.followup.send(embed=embed)
            return

        # Page 객체 생성
        pages = []
        for idx, (title, info) in enumerate(plans.items(), start=1):
            embed = Embed(title=f"{idx}번째 플랜", colour=discord.Color.green())
            embed.add_field(name="플랜 제목", value=title, inline=False)
            embed.add_field(name=":white_check_mark: 예약일시", value=info.get("start_date"), inline=False)
            embed.add_field(name=":scroll: 룰셋", value=str(info.get("ruleset")), inline=False)
            embed.add_field(name=":busts_in_silhouette: 최소 인원", value=str(info.get("min_players")), inline=False)
            members = ", ".join([f"<@{uid}>" for uid in info.get("players", [])]) or "없음"
            embed.add_field(name="플레이어", value=members, inline=False)
            embed.set_footer(text="Victoria3 KR Server")
            pages.append(Page(embed=embed, view=None))

        page_manager = PagesManager(pages)
        view = View()

        async def update_buttons(inter: discord.Interaction):
            """현재 페이지와 사용자 상태에 맞춰 버튼 재생성 및 플레이어 목록 갱신"""
            view.clear_items()
            current_page = page_manager.current_page
            embed = current_page.embed
            title = next((f.value for f in embed.fields if f.name == "플랜 제목"), None)
            user_id = str(inter.user.id)
            plans = load_file("database", "multi.json")

            # 임베드 플레이어 목록 업데이트
            if title in plans:
                members = ", ".join([f"<@{uid}>" for uid in plans[title].get("players", [])]) or "없음"
                for i, field in enumerate(embed.fields):
                    if field.name == "플레이어":
                        embed.set_field_at(i, name="플레이어", value=members, inline=False)
                        break

            # 이전 버튼
            prev_btn = Button(label="◀", style=discord.ButtonStyle.secondary)
            async def prev_callback(prev_inter):
                page_manager.prev_page()
                await update_buttons(prev_inter)
                await prev_inter.response.edit_message(embed=page_manager.current_page.embed, view=view)
            prev_btn.callback = prev_callback
            view.add_item(prev_btn)

            # 다음 버튼
            next_btn = Button(label="▶", style=discord.ButtonStyle.primary)
            async def next_callback(next_inter):
                page_manager.next_page()
                await update_buttons(next_inter)
                await next_inter.response.edit_message(embed=page_manager.current_page.embed, view=view)
            next_btn.callback = next_callback

            # 예약 / 예약 취소 버튼
            if title in plans and user_id in plans[title]["players"]:
                cancel_btn = Button(label="예약 취소", style=discord.ButtonStyle.danger)

                async def cancel_callback(inter2: discord.Interaction):
                    await inter2.response.defer(ephemeral=True)
                    plans = load_file("database", "multi.json")

                    if title not in plans or user_id not in plans[title]["players"]:
                        await inter2.followup.send("예약이 존재하지 않습니다.", ephemeral=True)
                        return
                    
                    if user_id == plans[title]["host_id"]:
                        await inter2.followup.send("호스트는 예약을 취소할 수 없습니다.", ephemeral=True)
                        return

                    # player_info / occupied_nations / 닉네임 복원
                    entry = next((e for e in plans[title]["player_info"] if e.startswith(f"{user_id}|")), None)
                    if entry:
                        plans[title]["player_info"].remove(entry)
                        _, user_name, country = entry.split("|", 2)
                        if country in plans[title]["occupied_nations"]:
                            plans[title]["occupied_nations"].remove(country)
                        member = inter2.guild.get_member(int(user_id))
                        if member and not member.guild_permissions.administrator:
                            await member.edit(nick=user_name)

                    plans[title]["players"].remove(user_id)
                    plans[title]["current_players"] -= 1
                    save_file("database", "multi.json", plans)

                    await update_buttons(inter2)
                    await inter2.followup.send(f"`{title}`에서 예약이 취소되었습니다.", ephemeral=True)

                cancel_btn.callback = cancel_callback
                view.add_item(cancel_btn)
            else:
                reserve_btn = Button(label="예약", style=discord.ButtonStyle.success)

                async def reserve_callback(inter2: discord.Interaction):
                    await inter2.response.defer(ephemeral=True)
                    plans = load_file("database", "multi.json")
                    if title in plans and user_id not in plans[title]["players"]:
                        plans[title]["players"].append(user_id)
                        plans[title]["current_players"] += 1
                        save_file("database", "multi.json", plans)

                        # 임베드 플레이어 목록 업데이트
                        members = ", ".join([f"<@{uid}>" for uid in plans[title]["players"]]) or "없음"
                        for i, field in enumerate(embed.fields):
                            if field.name == "플레이어":
                                embed.set_field_at(i, name="플레이어", value=members, inline=False)
                                break

                        await update_buttons(inter2)
                        await inter2.followup.send(f"{interaction.user.mention}님이 `{title}`에 참전!")

                reserve_btn.callback = reserve_callback
                view.add_item(reserve_btn)

            view.add_item(next_btn)

        # 최초 버튼 세팅 및 메시지 전송
        await update_buttons(interaction)
        await interaction.followup.send(embed=page_manager.current_page.embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduleShowSlash(bot))

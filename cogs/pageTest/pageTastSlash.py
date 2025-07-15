import discord
from discord.ext import commands
from discord import app_commands, Embed
from utils.page import Page, Pages
from discord.ui import Button, View, Select
from discord import SelectOption

class PageTestSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="page_test", description="페이지 시스템을 테스트합니다.")
    async def testing(self, interaction: discord.Interaction):
        select_options = [
            SelectOption(label="옵션 1", value="1"),
            SelectOption(label="옵션 2", value="2")
        ]

        pages = [
            Page(
                Embed(title="페이지 1", description="이것은 첫 번째 페이지입니다."),
                View(timeout=None).add_item(Button(label="테스트1", disabled=True))
            ),
            Page(
                Embed(title="페이지 2", description="이것은 두 번째 페이지입니다."),
                View(timeout=None).add_item(Select(custom_id="test1", options=select_options))
            ),
            Page(
                Embed(title="페이지 3", description="이것은 세 번째 페이지입니다."),
                View(timeout=None)
                    .add_item(Select(custom_id="test2", options=select_options))
                    .add_item(Button(label="테스트2", disabled=True))
            )
        ]

        page_manager = Pages(*pages)
        await interaction.response.send_message(embed=page_manager.current_page.embed, view=page_manager.current_page.view)

async def setup(bot: commands.Bot):
    await bot.add_cog(PageTestSlash(bot))
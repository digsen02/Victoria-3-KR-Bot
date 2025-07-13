import discord
from discord.ext import commands
from discord import app_commands, Embed
from utils.page import Page, Pages

class PageTestSlash(commands.Cog):
    def __init__(self, bot:commands.Cog):
        self.bot = bot



    @app_commands.command(name="page_test", description="페이지 시스템을 테스트합니다.")
    async def testing(self, interaction: discord.Interaction):
        page1 = Page(
            Embed(title="페이지 1", description="이것은 첫 번째 페이지입니다.")
        )

        page2 = Page(
            Embed(title="페이지 2", description="이것은 두 번째 페이지입니다.")
        )

        page3 = Page(
            Embed(title="페이지 3", description="이것은 세 번째 페이지입니다.")
        )
        pages = Pages(page1, page2, page3)

        print(pages.current_page.embed.title)
        print(bool(pages.current_page.view))

        await interaction.response.send_message(embed=pages.current_page.embed, view=pages.current_page.view)

async def setup(bot):
    await bot.add_cog(PageTestSlash(bot))
import discord
from discord.ext import commands
from discord import app_commands, Embed
from utils.page import Page, Pages
from discord.ui import Button, View, Select, item

class PageTestSlash(commands.Cog):
    def __init__(self, bot:commands.Cog):
        self.bot = bot



    @app_commands.command(name="page_test", description="페이지 시스템을 테스트합니다.")
    async def testing(self, interaction: discord.Interaction):
        view1 = View()
        button1 = Button(label="테스트1", disabled=True)
        select1 = Select(custom_id="test1")
        view1.add_item(button1)
        page1 = Page(
            Embed(title="페이지 1", description="이것은 첫 번째 페이지입니다."),
            *view1
        )

        view2 = View()
        view2.add_item(select1)




        page2 = Page(
            Embed(title="페이지 2", description="이것은 두 번째 페이지입니다."),
            *view2
        )

        view3 = View()

        select2 = Select(custom_id="test1")
        button2 = Button(label="테스트2", disabled=True)

        view3.add_item(select2)
        view3.add_item(button2)

        page3 = Page(
            Embed(title="페이지 3", description="이것은 세 번째 페이지입니다."),
            *view3
        )
        pages = Pages(page1, page2, page3)


        await interaction.response.send_message(embed=pages.current_page.embed, view=pages.current_page.view)

async def setup(bot):
    await bot.add_cog(PageTestSlash(bot))
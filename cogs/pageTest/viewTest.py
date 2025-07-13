import discord
from discord.ext import commands
from discord import app_commands, Embed
from utils.page import Page, Pages
from discord.ui import Button, View, Select, item


class ViewTestSlash(commands.Cog):
    def __init__(self, bot:commands.Cog):
        self.bot = bot



    @app_commands.command(name="view_test", description="view 시스템을 테스트합니다.")
    async def testing(self, interaction: discord.Interaction):
        embed1 = Embed(title="view 테스트")
        button1 = Button(label="label", disabled= False)
        view = View()
        view.add_item(button1)

        await interaction.response.send_message(embed= embed1, view=view)

async def setup(bot):
    await bot.add_cog(ViewTestSlash(bot))
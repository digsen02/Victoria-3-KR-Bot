from discord.ext import commands
from discord import app_commands

class GreetingSlash(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot
    @app_commands.command(name="hello", description="안녕하세요!")
    async def greeting(self, interaction):
        await interaction.response.send_message("안녕하세요!")

async def setup(bot):
    await bot.add_cog(GreetingSlash(bot))
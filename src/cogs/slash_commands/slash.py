import discord

from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name='introduce',
        description='Introduce yourself!')
    async def introduce(
        self,
        interaction: discord.Interaction,
        name: str,
        age: int) -> None:
        await interaction.response.send_message(f'Your name is: {name} and your age is {age}')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        SlashCommands(bot),
        guilds = [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)])
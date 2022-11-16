import discord
import traceback

from discord import app_commands
from discord.ext import commands

class TestM(discord.ui.Modal, title="Test"):
    name = discord.ui.TextInput(
        label='Cats',
        placeholder='Say something about what you like here!',
    )

    feedback = discord.ui.TextInput(
        label='What do you think of this server?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)


    @discord.ui.button(label="ClickMe", style=discord.ButtonStyle.grey)
    async def clickme(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TestM())


class ModelTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def btest(self, ctx):
        await ctx.reply('Message with a button', view=Buttons())

async def setup(bot):
    await bot.add_cog(ModelTesting(bot))
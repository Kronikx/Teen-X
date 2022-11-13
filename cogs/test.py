import discord

from discord.ext import commands

# Buttons subclasess
class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Send Message', style=discord.ButtonStyle.grey, custom_id='menu:1')
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Grey Button")

    @discord.ui.button(label='Edit Message', style=discord.ButtonStyle.green, custom_id='menu:2')
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Green Button")

    @discord.ui.button(label='Embed', style=discord.ButtonStyle.blurple, custom_id='menu:3')
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        em = discord.Embed(color=discord.Color.random())
        em.set_author(name=f'testing button shit')
        em.add_field(name='idk', value='test')
        await interaction.response.send_message(embed=em)

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.grey, custom_id='menu:4')
    async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
        em = discord.Embed(color=discord.Color.random())
        em.set_author(name=f'Goodbye')
        em.add_field(name='Bye BYe', value='test')
        await interaction.response.edit_message(embed=em)
        self.value = False
        self.stop()

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def menu(self, ctx):
        await ctx.reply("Test Test Test", view=Menu())

async def setup(bot):
    await bot.add_cog(Test(bot))
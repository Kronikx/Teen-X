import discord
import asyncio

from discord import ui
from discord.ext import commands

class Questionnaire(ui.Modal, title='Explanation.'):
    name = ui.TextInput(label='Topic: ', placeholder='Briefly Explain why you made this ticket....', required=True,)
    answer = ui.TextInput(label='Additional Information: ', placeholder='Use this to add additional information.....', style=discord.TextStyle.long, required=False, max_length=300,)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {interaction.user.name}! A staff member will with you soon.', ephemeral=True)
        
        em = discord.Embed()
        em.set_author(name='Ticket creation reason')
        em.add_field(name='Topic:', value=self.name.value)
        em.add_field(name='Additional Information:', value=self.answer.value) if self.answer.value else None
        
        await interaction.channel.send(embed=em)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Explain', style=discord.ButtonStyle.grey, custom_id='bae:explainbtn', emoji='⌨️')
    async def explain(self, interaction: discord.Interaction, button: discord.ui.Button):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(send_messages=True)
            }

        await interaction.response.send_modal(Questionnaire())
        await interaction.channel.edit(overwrites=overwrites)
        button.disabled = True
        await interaction.edit_original_message(view=self)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.grey, custom_id='bae:claimbtn', emoji='✅')
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{interaction.user} has claimed this ticket.')

    @discord.ui.button(label="Close", style=discord.ButtonStyle.grey, custom_id='bae:closebtn', emoji='🔒')
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Closing')
        await asyncio.sleep(20)
        await interaction.channel.delete()

class Open(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open", style=discord.ButtonStyle.grey, custom_id='bae:openbtn', emoji='🎫')
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }

        for c in interaction.guild.categories:
            if 'tickets' in c.name.lower():
                await interaction.response.send_message('Ticket created!', ephemeral=True)
                ch = await c.create_text_channel(name=f'ticket-{interaction.user.name}', overwrites=overwrites)

                em = discord.Embed(description="Welcome! A staff member will be with you shortly.\nPlease click the 'Explain' button and follow the prompts within.")
                em.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)

                await ch.send(embed=em, view=Buttons())

class Tickets(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    # em = discord.Embed(description='Welcome! A staff member will be with you shortly. Do not ping any staff individuals, just be patient and explain what you need.')
    # em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

    @commands.group(name='Tickets', invoke_without_command=True)
    async def _tickets(self, ctx):
        msg = await ctx.send(f'Starting ticket system process.')
        
        c = await ctx.guild.create_category(name='Tickets')
        ch = await c.create_text_channel(name=f'Tickets')

        em = discord.Embed(title='Open a Ticket', description=f'Click the button below to open a ticket')
        em.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        

        await ch.send(embed=em, view=Open())
        await msg.edit(content=f'Ticket system created.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tickets(bot))
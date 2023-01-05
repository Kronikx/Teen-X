import discord

from discord.ext import commands
from cogs.embeds import sendtologs
from ext.Paginator.paginator import PaginatorView

owners = [896075048228634655, 168376879479390208, 756297040014606345]

class Completed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Completed', style=discord.ButtonStyle.green, custom_id='todo2:1', emoji="✅", disabled=True)
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class Canceled(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Canceled', style=discord.ButtonStyle.grey, custom_id='todo2:1', emoji="❌", disabled=True)
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class Todo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Complete', style=discord.ButtonStyle.green, custom_id='todo:1', emoji="✅")
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=Completed())

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey, custom_id='todo:2', emoji="❌")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=Canceled())

class Owner(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command(name='todo', hidden=True)
    @commands.is_owner()
    async def _todo(self, ctx, *, todo: str):
        if todo is None:
            await ctx.send("Need you to give me something to add.")
        else:
            em = discord.Embed(color=0xb6bbf9)
            em.add_field(name='Todo:', value=f'```py\n{todo}\n```')
            todo_chan = self.bot.get_channel(1043945403483172945)

            await todo_chan.send(embed=em, view=Todo())
            await ctx.message.add_reaction('✅')

    @commands.command(name='cogs', hidden=True)
    @commands.is_owner()
    async def _cogs(self, ctx):
        ext = []
        end = ''
        for cog in self.bot.cogs:
            ext.append(cog)
        for e in ext:
            end += e + ' '
        eend = end.replace(' ', ', ')
        await ctx.reply(f'List of loaded cogs: `{eend}({len(self.bot.cogs)})`')

    @commands.command()
    async def guilds(self, ctx):
        embeds = []
        for guilds in discord.utils.as_chunks(self.bot.guilds, 1):
            embed = discord.Embed(title="List of all guilds")
            for g in guilds:
                embed.set_thumbnail(url=g.icon) if g.icon else None
                embed.add_field(name=f"Guild Information", value=f"**Owner:** {g.owner.mention}\n**Guild ID:** `{g.id}`\n**Created:** `{g.created_at}`\n**Roles:** `{len(g.roles)}`\n**Humans:** `{len([m for m in g.members if not m.bot])}`\n**Bots:** `{len([m for m in g.members if m.bot])}`")
            embeds.append(embed)

        view = PaginatorView(embeds)
        await ctx.send(embed=view.initial, view=view)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.load_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'`Failed to load {ext}`')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Loaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.load_extension(f'cogs.{extension}')
                await ctx.reply(f'`Loaded {extension}`')
            except Exception as e:
                await ctx.reply(f'`Failed to load {extension}`')
                await sendtologs(self.bot, type='error', msg=e)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.unload_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'`Failed to unload {ext}`')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Unloaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.unload_extension(f'cogs.{extension}')
                await ctx.reply(f'`Unloaded {extension}`')
            except Exception as e:
                await ctx.reply(f'`Failed to unload {extension}`')
                await sendtologs(self.bot, type='error', msg=e)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.reload_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'`Failed to reload {ext}`')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Reloaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.reload_extension(f'cogs.{extension}')
                await ctx.reply(f'`Reloaded {extension}`')
            except Exception as e:
                await ctx.reply(f'`Failed to reload {extension}`')
                await sendtologs(self.bot, type='error', msg=e)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Owner(bot))
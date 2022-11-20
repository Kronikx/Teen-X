import discord

from discord.ext import commands
from typing import Optional, Literal
from ext.functions import sendtologs

owners = [168376879479390208, 459439879269646358, 876344421656981544, 948796139954655235, 896075048228634655]

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

            await todo_chan.send(embed=em)
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

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.load_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'Failed to load {ext}')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Loaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.load_extension(f'cogs.{extension}')
                await ctx.reply(f'`Loaded {extension}`')
            except Exception as e:
                await ctx.reply(f'Failed to load {extension}')
                await sendtologs(self.bot, type='error', msg=e)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.unload_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'Failed to unload {ext}')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Unloaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.unload_extension(f'cogs.{extension}')
                await ctx.reply(f'`Unloaded {extension}`')
            except Exception as e:
                await ctx.reply(f'Failed to unload {extension}')
                await sendtologs(self.bot, type='error', msg=e)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, extension):
        if len(extension.split()) > 1:
            for ext in extension.split():
                try:
                    await self.bot.reload_extension(f'cogs.{ext}')
                except Exception as e:
                    await ctx.reply(f'Failed to reload {ext}')
                    await sendtologs(self.bot, type='error', msg=e)
                    continue
            await ctx.reply(f'Reloaded {extension.replace(" ", ", ")}')
        else:
            try:
                await self.bot.reload_extension(f'cogs.{extension}')
                await ctx.reply(f'`Reloaded {extension}`')
            except Exception as e:
                await ctx.reply(f'Failed to reload {extension}')
                await sendtologs(self.bot, type='error', msg=e)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Owner(bot))
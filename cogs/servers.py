from discord.ext import commands
from colorama import init, Fore

init(autoreset=True)

class Servers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name='prefix', with_app_command=True)
    async def _prefix(self, ctx):
        data = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE id = $1", ctx.guild.id)
        if data:
            prefix = data[0]
        else:
            prefix = '-'
        await ctx.reply(f'Prefix for **{ctx.guild.name}**: `{prefix}`')

    @commands.hybrid_command(name='addprefix', with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def _padd(self, ctx, prefix = None):
        if prefix is None:
            return
        data = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE id = $1", ctx.guild.id)
        if data:
            await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE id = $2", prefix, ctx.guild.id)
            await ctx.reply(f'Updated prefix to: `{prefix}`')
        else:
            await self.bot.db.execute("INSERT INTO guilds (prefix) VALUES ($1)", prefix)
            await ctx.reply(f'Set prefix to: `{prefix}`')

    @commands.hybrid_command(name='delprefix', with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def _pdel(self, ctx):
        data = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE id = $1", ctx.guild.id)
        if data:
            await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE id = $2", '-', ctx.guild.id)
        else:
            pass
        await ctx.reply(f'Removed this guilds custom prefix.')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Servers(bot))
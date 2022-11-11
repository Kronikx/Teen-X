import discord

from discord.ext import commands
from colorama import init, Fore
from utils.functions import sendtologs

class Database(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def check(self, ctx):
        try:
            for g in self.bot.guilds:
                if g.id == 1037005626112491522:
                    pass
                else:
                    ids = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE id = $1", g.id)
                    if ids == None:
                        await g.leave()
                        await sendtologs(self, type='guild', msg=f'Left Guild: {g.name}({g.id})\nGuild not permitted.')
                    else:
                        pass
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await sendtologs(self, type='error', msg=e)


    @commands.group(name='database', aliases=['db'], hidden=True)
    @commands.is_owner()
    async def _db(self, ctx):
        try:
            p = await self.bot.db.fetchrow("SELECT * FROM guilds")
            await ctx.send(p, delete_after=10)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(f'[Database] {e}')
            await sendtologs(self, type='database', msg=e)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Database(bot))
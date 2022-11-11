from datetime import datetime
from discord.ext import commands
from utils.functions import sendtologs

class Notes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(name="notes")
    async def _notes(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                notes = await self.bot.db.execute("SELECT * FROM notes WHERE owner_id = $1", ctx.author.id)
                await ctx.send(notes)
            except Exception as e:
                print(e)
                await sendtologs(self, type='database', msg=e)

    @_notes.command(name="add")
    async def _add(self, ctx, *, note):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        try:
            await self.bot.db.execute("INSERT INTO notes (timestamp, contents, owner_id) VALUES ($1, $2, $3)", timestamp, note, ctx.author.id)
            await ctx.send(f"Added Note.")
        except Exception as e:
            print(e)
            await sendtologs(self, type='database', msg=e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Notes(bot))
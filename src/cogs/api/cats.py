import aiohttp
import discord

from decouple import config
from discord.ext import commands

class CatAPI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_key = config("cats_api_key")

    # {"breeds":[],"id":"bq4","url":"https://cdn2.thecatapi.com/images/bq4.jpg","width":600,"height":800}

    @commands.hybrid_command(name='cat', with_app_command=True)
    @commands.guild_only()
    async def _cat(self, ctx):
        """Get stats on cats."""
        async with aiohttp.ClientSession as session:
            async with session.get(f"https://api.thecatapi.com/v1/images/search?limit=1&api_key={self.api_key}") as api:
                data = api.json()

                cat_image = data["url"]

                await ctx.reply(cat_image)

async def setup(bot):
    await bot.add_cog(
        CatAPI(bot),
        guilds = [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)]
    )
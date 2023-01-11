import animec
import discord

from discord import app_commands
from discord.ext import commands
from cogs.embeds import Embeds

class Esther(commands.Cog):
    """Anime commands so that we can keep our active dev badges !"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="Anime")
    @commands.guild_only()
    async def _anime(self, ctx, *, anime: str):
        """Query data about anime"""
        msg = await ctx.reply(f"Quering the API for: `{anime}`")
        result = animec.Anime(anime)

        if result:
            embed = discord.Embed(title=f"{result.name} ({result.title_english})", url=result.url, description=f"{result.description[:200]}...")
            embed.set_thumbnail(url = result.poster)
            embed.add_field(name="Episodes", value=result.episodes, inline=True)
            embed.add_field(name="Aired", value=result.aired, inline=True)
            embed.add_field(name="Type", value=result.type, inline=True)
            embed.add_field(name="Popularity", value=result.popularity, inline=True)
            embed.add_field(name="Ranked", value=result.ranked, inline=True)
            embed.add_field(name="Status", value=result.status, inline=True)
            embed.add_field(name="Rating", value=result.rating, inline=True)
            embed.add_field(name="Favorites", value=result.favorites, inline=True)
            embed.add_field(name="Nsfw Status", value=result.is_nsfw(), inline=True)

            if result.teaser:
                embed.set_footer(text="Note: Teaser listed below may not be accurate.")
                view = discord.ui.View()
                view.add_item(discord.ui.Button(label='Teaser', emoji="🖥️", style=discord.ButtonStyle.link, url=result.teaser))

            await msg.edit(content = None, embed = embed, view = view)
        else: await msg.edit(content=None, embed = Embeds().error("No data was returned from API"))


async def setup(bot) -> None:
    await bot.add_cog(Esther(bot))

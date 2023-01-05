import discord

from discord.ext import commands
from ext.Paginator.paginator import PaginatorView

class Tests(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        embeds = []
        for roles in discord.utils.as_chunks(ctx.guild.roles, 5):
            embed = discord.Embed(title="List of roles")
            for i in roles:
                embed.add_field(name=f"{i.name}", value=f"Total members: `{len(i.members)}`")
            embeds.append(embed)

        view = PaginatorView(embeds)
        await ctx.send(embed=view.initial, view=view)

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

async def setup(bot):
    await bot.add_cog(Tests(bot))
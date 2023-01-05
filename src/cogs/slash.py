import discord

from typing import Optional, Literal
from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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

    @app_commands.command(
        name='introduce',
        description='Introduce yourself!')
    async def introduce(
        self,
        interaction: discord.Interaction,
        name: str,
        age: int) -> None:
        await interaction.response.send_message(f'Your name is: {name} and your age is {age}')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        SlashCommands(bot),
        guilds = [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)])
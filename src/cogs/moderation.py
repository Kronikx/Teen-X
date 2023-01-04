import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="nickname", description="Change a users nickname.", aliases=['nick'])
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.has_guild_permissions(manage_nicknames=True)
    async def _nick(self, ctx, member: discord.Member = None, nickname: str = None):
        if member is None:
            member = ctx.author

        try:
            if nickname is None:
                if member.nick != None:
                    await member.edit(nick=None)
                    await ctx.send(f"Reset {member.mention}'s nickname")
                else:
                    await ctx.send("No nickname provided.")
            else:
                await member.edit(nick=nickname)
                await ctx.send(f"Set {member.mention} nickname to: {nickname}")
        except discord.Forbidden:
            await ctx.send(f"You do not have the required permissions to edit this user's nickname")

    @commands.command(name='purge', aliases=['p', 'c', 'clear'])
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, amount: int = 2000):
        if amount > 2000:
            amount = 2000

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
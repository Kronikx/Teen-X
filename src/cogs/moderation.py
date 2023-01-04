import discord
from discord import abc
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

    @commands.command(name="cleanup", aliases=['bc'])
    @commands.has_guild_permissions(manage_messages=True)
    async def _cleanup(self, ctx):
        def is_bot(m):
            return (m.webhook_id is None and m.author.bot) or (ctx.prefix and m.content.startswith(ctx.prefix))

        await ctx.message.delete()
        await ctx.channel.purge(limit=1000, check=is_bot, bulk=True)

    @commands.group(name='purge', aliases=['p', 'c', 'clear'], invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, member: discord.Member = None, amount: int = 2000):
        if amount > 2000:
            amount = 2000
        

        if member is None:
            def is_author(m):
                return None
        else:
            def is_author(m):
                return m.author == ctx.author

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True, check=is_author)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
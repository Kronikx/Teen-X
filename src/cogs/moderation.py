import discord

from cogs.embeds import Embeds
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.embeds = Embeds()

    @commands.command(name="nickname", aliases=['nick'])
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.has_guild_permissions(manage_nicknames=True)
    async def _nick(self, ctx, member: discord.Member = None, *, nickname: str = None):
        """Change a users nickname."""
        if member is None:
            member = ctx.author

        if nickname is None:
            if member.nick != None:
                await member.edit(nick=None)
                embed = self.embeds.success(f"Reset {member.mention}'s nickname")
            else:
                embed = self.embeds.error(f"`nickname` is a required argument!")
        else:
            await member.edit(nick=nickname)
            embed = self.embeds.success(f"Set {member.mention} nickname to: {nickname}")

        await ctx.send(embed = embed)

    @commands.command(name="cleanup", aliases=['bc'])
    @commands.has_guild_permissions(manage_messages=True)
    async def _cleanup(self, ctx):
        """Clear all bot messages"""
        def is_bot(m):
            return (m.webhook_id is None and m.author.bot) or (ctx.prefix and m.content.startswith(ctx.prefix))

        await ctx.message.delete()
        await ctx.channel.purge(limit=2000, check=is_bot, bulk=True)

    @commands.group(name='purge', aliases=['p', 'c', 'clear'], invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, amount: int = None):
        """Clear a certain amount of messages in a certain channel."""
        if amount > 2000:
            amount = 2000

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True)

    @_purge.command(name="after", aliases = ['upto'], invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _after(self, ctx, after: discord.Message = None):
        """Clear all messages after the given message link/ID"""
        
        await ctx.message.delete()
        await ctx.channel.purge(limit=None, after=after, bulk=True)

    @_purge.command(name="between", invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _between(self, ctx, start: discord.Message = None, end: discord.Message = None):
        """Clear all messages between the given message link/ID"""
        
        await ctx.message.delete()
        await ctx.channel.purge(limit=None, after=start, before=end, bulk=True)

    @_purge.command(name="before", invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def _before(self, ctx, before: discord.Message = None):
        """Clear all messages before the given message link/ID"""
        
        await ctx.message.delete()
        await ctx.channel.purge(limit=None, before=before, bulk=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
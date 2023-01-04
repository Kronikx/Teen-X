import time
import discord

from discord.ext import commands
from cogs.functions import sendtologs

class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=200)

class Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def _ping(self, ctx):
        """Display the bots ping."""
        try:
            t_1 = time.perf_counter()
            await ctx.channel.typing() # Getting API ping
            t_2 = time.perf_counter()
        except Exception as e:
            await sendtologs(self.bot, type='error', msg=e)
            pass

        api_ping = round((t_2-t_1)*1000)
        web_ping = round(self.bot.latency * 1000, 2)

        await ctx.reply(f'<a:typing:1040254641121804359> **{api_ping}ms**\n<:discord:1040254738433847317> **{web_ping}ms**')
    
    @commands.command(name='avatar', aliases=['av', 'pfp'])
    async def _avatar(self, ctx, user: discord.User = None):
        """Display someones avatar."""
        if user == None:
            user = ctx.author

        link = user.avatar if user.avatar else user.default_avatar

        em=discord.Embed(color=ctx.author.color)
        em.set_author(name=f"{user}'s avatar", url=link.url)
        em.set_image(url=link.url)

        view = Buttons()
        view.add_item(discord.ui.Button(label="Image URL", style=discord.ButtonStyle.link, url=link.url))
        await ctx.reply(embed=em, view=view)

    @commands.command(name='banner', aliases=['ub', 'userbanner'])
    async def _banner(self, ctx, user: discord.User = None):
        """Display someones banner."""
        if user == None:
            user = ctx.author
        user = await self.bot.fetch_user(user.id)
        if user.banner:
            em = discord.Embed(color=ctx.author.color)
            em.set_author(name=f"{user.name}'s banner", url=user.banner.url)
            em.set_image(url=user.banner.url)

            view = Buttons()
            view.add_item(discord.ui.Button(label="Image URL", style=discord.ButtonStyle.link, url=user.banner.url))
            await ctx.reply(embed=em, view=view)
        else:
            await ctx.reply(f'{user} has no banner.')

    @commands.command(name="serveravatar", aliases=['sav'])
    async def _serveravatar(self, ctx, *, member: discord.Member = None):
        """Gives you a user's guild avatar if available."""
        if member == None:
            member = ctx.author
        if member.guild_avatar == None:
            await ctx.reply(f'{member.mention} has no Server Avatar.')
        else:
            av=discord.Embed(color=ctx.author.color)
            av.set_author(name=f"{member}'s server avatar", url=member.guild_avatar, icon_url=member.display_avatar)
            av.set_image(url=member.guild_avatar)

            view = Buttons()
            view.add_item(discord.ui.Button(label="Image URL", style=discord.ButtonStyle.link, url=member.guild_avatar.url))
            await ctx.reply(embed=av, view=view)

    @commands.hybrid_command(name="whois",  aliases=['ui', 'userinfo'])
    async def _whois(self, ctx, user: discord.User = None):
        """Find information about a member."""
        if user is None:
            user = ctx.author
        member = ctx.guild.get_member(user.id)
        # Information variables
        bot = True if user.bot else False
        Mutuals = len(user.mutual_guilds) if user.mutual_guilds else 0
        # Guild Variables
        if member is not None:
            pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
            roles = []
            for role in member.roles:
                roles.append(role.mention)

        em = discord.Embed(description=f"**User Information:** {user.mention}", color=ctx.author.color)
        em.set_thumbnail(url=user.display_avatar)
        em.add_field(name="Information", value=f"**Name:** `{user}`\n**ID:** `{user.id}`\n**Is Bot:** `{bot}`\n**Created:** <t:{int(user.created_at.timestamp())}:R>\n**Guilds:** `{Mutuals} Shared`", inline=True)
        em.add_field(name="Guild Related", value=f"**Joined:** <t:{int(ctx.author.joined_at.timestamp())}:R>\n**Join Pos:** `{pos}/{len(ctx.guild.members)}`\n**Top Role:** {roles[1]}\n**Color:** `{member.color}`", inline=True) if member else None
        await ctx.send(embed=em)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Users(bot),
        guilds= [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)])
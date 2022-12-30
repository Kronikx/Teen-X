import time
import discord

from discord.ext import commands
from ext.functions import sendtologs

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
    async def _avatar(self, ctx, usr: discord.User = None):
        """Display someones avatar."""
        if usr == None:
            usr = ctx.author
        if usr.avatar:
            def__av = usr.avatar
            av=discord.Embed(color=0x2f3136)
            av.set_author(name=f"{usr}'s avatar", url=def__av)
            av.set_image(url=def__av)
            await ctx.reply(embed=av)
        else:
            def_av = usr.default_avatar
            defav=discord.Embed(color=0x2f3136)
            defav.set_author(name=f"{usr}'s avatar", url=def_av)
            defav.set_image(url=def_av)
            await ctx.reply(embed=defav)

    @commands.command(name='banner', aliases=['ub', 'userbanner'])
    async def _banner(self, ctx, usr: discord.User = None):
        """Display someones banner."""
        if usr == None:
            usr = ctx.author
        usr = await self.bot.fetch_user(usr.id)
        if usr.banner:
            em = discord.Embed(color=0x2f3136)
            em.set_author(name=f"{usr.name}'s banner", url=usr.banner.url)
            em.set_image(url=usr.banner.url)
            await ctx.reply(embed=em)
        else:
            await ctx.reply(f'{usr} has no banner.')

    @commands.command(name="serveravatar", aliases=['sav'])
    async def _serveravatar(self, ctx, *, member: discord.Member = None):
        """Gives you a user's guild avatar if available."""
        if member == None:
            member = ctx.author
        if member.guild_avatar == None:
            await ctx.reply(f'{member.mention} has no Server Avatar.')
        else:
            av=discord.Embed(color=0x2f3136)
            av.set_author(name=f"{member}'s server avatar", url=member.guild_avatar, icon_url=member.display_avatar)
            av.set_image(url=member.guild_avatar)
            await ctx.reply(embed=av)

    @commands.hybrid_command(name="whois",  aliases=['ui', 'userinfo'])
    async def _whois(self, ctx, usr: discord.User = None):
        """Find information about a user."""
        if usr == None:
            usr = ctx.author
        em=discord.Embed(description=f'{usr}(`{usr.id}`)', color=0x2f3136)
        if usr.bot == True: 
            em.add_field(name="Profile", value=f'`Name:` {usr.name}\n`Discrim:` #{usr.discriminator}\n`Bot:` <:The_greenTick:985459545033818112>', inline=True)
        else:
            em.add_field(name="Profile", value=f'`Name:` {usr.name}\n`Discrim:` #{usr.discriminator}\n`Bot:` <:the_wrong:984091444774060042>', inline=True)
        if usr.avatar:
            em.set_thumbnail(url=usr.avatar)
        else:
            em.set_thumbnail(url=usr.default_avatar)
        em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url, url=f"https://discord.com/users/{usr.id}")
        em.add_field(name='Created:',value=f'<t:{int(usr.created_at.timestamp())}:d>(<t:{int(usr.created_at.timestamp())}:R>)', inline=True)
        em.set_footer(text=f"{len(usr.mutual_guilds)} mutual guilds.") if usr.mutual_guilds else None
        await ctx.reply(embed=em)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Users(bot),
        guilds= [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)])
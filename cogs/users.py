import discord

from discord.ext import commands
from colorama import init, Fore

init(autoreset=True)

class Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(name='avatar', description='Display someones avatar.', aliases=['av', 'pfp'],  with_app_command=True)
    async def _avatar(self, ctx, usr: discord.User = None):
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

    @commands.hybrid_command(name='banner', description='Display someones banner.', aliases=['ub', 'userbanner'], with_app_command=True)
    async def _banner(self, ctx, usr: discord.User = None):
        if usr == None:
            usr = ctx.author
        usr = await self.bot.fetch_user(usr.id)
        print(f'{Fore.GREEN}Succesfully fetched user: {usr}')
        if usr.banner:
            em = discord.Embed(color=0x2f3136)
            em.set_author(name=f"{usr.name}'s banner", url=usr.banner.url)
            em.set_image(url=usr.banner.url)
            await ctx.reply(embed=em)
        else:
            await ctx.reply(f'{usr} has no banner.')

    @commands.hybrid_command(name="serveravatar", description='Gives you a user\'s guild avatar if available.', aliases=['sav'], with_app_command=True)
    async def _serveravatar(self, ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author
        if member.guild_avatar == None:
            await ctx.reply(f'{member.mention} has no Server Avatar.')
        else:
            av=discord.Embed(color=0x2f3136)
            av.set_author(name=f"{member}'s server avatar", url=member.guild_avatar, icon_url=member.display_avatar)
            av.set_image(url=member.guild_avatar)
            await ctx.reply(embed=av)

    @commands.hybrid_command(name="whois", description='Find information about a user.', aliases=['ui', 'userinfo'])
    async def _whois(self, ctx, usr: discord.User = None):
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
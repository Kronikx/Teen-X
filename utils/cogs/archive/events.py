import discord

from discord.ext import commands
from colorama import init, Fore
from utils.functions import sendtologs

init(autoreset=True)

class Events(commands.Cog):
    """All bot events."""
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.bot.process_commands(after)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await sendtologs(self, type='guild', msg=f'Joined a new guild {guild.name}({guild.id})')


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await sendtologs(self, type='guild', msg=f'Left guild {guild.name}({guild.id})')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound, commands.TooManyArguments)
        send_embed = (commands.MissingPermissions, commands.DisabledCommand, discord.HTTPException, commands.NotOwner,
                      commands.CheckFailure, commands.MissingRequiredArgument, commands.BadArgument,
                      commands.BadUnionArgument)

        errors = {
            commands.MissingPermissions: "You do not have the required permissions to use this command.",
            commands.DisabledCommand: "This command is currently disabled.",
            discord.HTTPException: "There was an error connecting to Discord. Please try again.",
            commands.CommandInvokeError: "There was an issue running the command.",
            commands.NotOwner: "You are not the owner.",
            commands.CheckFailure: "This command cannot be used in this guild!",
            commands.MissingRole: "You're missing the **{}** role",
            commands.MissingRequiredArgument: "`{}` is a required argument!"
        }

        if isinstance(error, ignored):
            return

        if isinstance(error, send_embed):
            if isinstance(error, commands.MissingRequiredArgument):
                err = errors.get(error.__class__).format(str(error.param).partition(':')[0])
            elif isinstance(error, commands.MissingRole):
                role = ctx.guild.get_role(error.missing_role)
                err = errors.get(error.__class__).format(role.mention)
            else:
                efd = errors.get(error.__class__)
                err = str(efd)
                if not efd:
                    err = str(error)

            em = discord.Embed(description = f"{str(err)}", color = discord.Colour.red())
            try:
                await ctx.send(embed = em)
                return
            except discord.Forbidden:
                pass

        # when error is not handled above
        em = discord.Embed(
            title = 'Bot Error:',
            description = f'```py\n{error}\n```',
            color = discord.Colour.red()
        )
        await ctx.send(embed = discord.Embed(description = f"`{error}`",
                                             color = discord.Colour.red()))
        print(f"{Fore.RED}[Error] {error}")
        await sendtologs(self, type='error', msg=error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
import discord

from cogs.embeds import Embeds
from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embeds = Embeds()

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

            embed = embeds.error(str(err))
            try:
                await ctx.send(embed = embed)
                return
            except discord.Forbidden:
                pass

        # when error is not handled above
        em = embeds.unhandled()
        await ctx.send(embed = em)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandling(bot))
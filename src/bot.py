import os
import asyncio
import discord

from decouple import config
from cogs.embeds import Embeds
from discord.ext import commands

os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing Jishaku underscores

initial_extensions = (
    'cogs.jsk',
    'cogs.owner',
    'cogs.moderation',
    'cogs.information'
)

class Slatt(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            message_content=True,
        )
        super().__init__(
            command_prefix= commands.when_mentioned_or(','),
            mentions = allowed_mentions,
            intents = intents,
            case_insensitive = True,
            chunk_guilds_at_startup=True,
            heartbeat_timeout=150.0,
            enable_debug_events=True,
        )

        self.embeds = Embeds()

    async def setup_hook(self) -> None:
        self.bot_app_info = await self.application_info()

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                # Send to logs or log to console
                # await loggingEmbed(self, type='error', msg=e)
                pass

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def on_message(self, message = discord.Message):
        await self.process_commands(message)

    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.process_commands(after)

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

            embed = self.embeds.error(str(err))
            try:
                await ctx.send(embed = embed)
                return
            except discord.Forbidden:
                pass

        # when error is not handled above
        em = self.embeds.unhandled()
        await ctx.send(embed = em)

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def close(self) -> None:
        await super().close()

    async def start(self) -> None:
        await super().start(config("TOKEN"), reconnect=True)

async def run_bot():
    async with Slatt() as bot:
        await bot.start()

asyncio.run(run_bot())

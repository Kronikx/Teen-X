import os
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

class Radical(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents(guilds=True, members=True, bans=True, emojis=True, messages=True, reactions=True, message_content=True)
        super().__init__(
            command_prefix= commands.when_mentioned_or('.'),
            case_insensitive = True,
            chunk_guilds_at_startup=True,
            heartbeat_timeout=150.0,
            enable_debug_events=True,
            strip_after_prefix = True,
            intents = intents,
            mentions = allowed_mentions,
        )

        self.bot_app_info = discord.AppInfo
        self.bot_guild = 1043940794450595890
        self.error_channel_id = 1043940794450595897
        self.token = config("TOKEN")

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    @property
    def error_channel(self) -> discord.TextChannel:
        return self.get_guild(self.bot_guild).get_channel(self.error_channel_id)

    async def setup_hook(self) -> None:
        self.bot_app_info = await self.application_info()

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                # Send to logs or log to console
                print(e)
                pass

    async def close(self) -> None:
        await super().close()

bot = Radical()

@bot.event
async def on_ready():
    # Add startup ASCII here or something
    print(f'Ready: {bot.user} (ID: {bot.user.id})')

# Error handler needs to be rewritten
@bot.event
async def on_command_error(ctx, error):
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

        embed = Embeds().error(str(err))
        try:
            await ctx.send(embed = embed)
            return
        except discord.Forbidden:
            pass

    # when error is not handled above
    em = Embeds().unhandled()
    await ctx.send(embed = em)

@bot.event
async def on_message(message = discord.Message):
        await bot.process_commands(message)

@bot.event
async def on_message_edit(before = discord.Message, after = discord.Message):
    if after.embeds or before.embeds:
        return
    if after.author.id == before.author.id:
        return await bot.process_commands(after)

bot.run(token=config("TOKEN"), reconnect=True)

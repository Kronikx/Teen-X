from __future__ import annotations

from utils.functions import sendtologs
from discord.ext import commands
import discord
import os
import time
import aiohttp
import logging
import json
from typing import Any
from decouple import config


os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing underscores
log = logging.getLogger(__name__)

initial_extensions = (
    'jishaku',
    'cogs.owner',
    'cogs.misc',
    'cogs.users',
)

class Slatt(commands.Bot):
    user: discord.ClientUser
    logging_handler: Any
    bot_app_info: discord.AppInfo

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
            command_prefix= commands.when_mentioned_or('-'),
            mentions = allowed_mentions,
            intents = intents,
            case_insensitive = True,
            application_id = 1040566823579566160,
            chunk_guilds_at_startup=False,
            heartbeat_timeout=150.0,
            enable_debug_events=True,
        )

        self.client_key = 1040566823579566160

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()
        # self.bot_app_info = await self.application_info()
        self.owner_ids = [168376879479390208, 459439879269646358, 876344421656981544]

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                log.exception('Falied to load extension %s.', extension)

    # @property
    # def owner(self) -> discord.User:
        # return self.bot_app_info.owner

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
        await sendtologs(self, type='error', msg=error)

    async def on_message(self, message = discord.Message):
        await self.process_commands(message)

    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.process_commands(after)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = discord.utils.utcnow()
            log.info('Ready: %s (ID: %s)', self.user, self.user.id)

    async def close(self) -> None:
        await super().close()
        await self.session.close()

    async def start(self) -> None:
        await super().start(config("TOKEN"), reconnect=True)


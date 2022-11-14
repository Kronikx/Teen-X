from __future__ import annotations

from discord.ext import commands
import discord
import os
import time
import aiohttp
import logging
from decouple import config
from typing import Any

os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing underscores
log = logging.getLogger(__name__)

initial_extensions = (
    'jishaku',
    'cogs.owner.owner',
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
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id
        
        goingupmsg = f'<a:typing:1040254641121804359> Starting up at....... <t:{int(time.time())}:F>'
        await self.SendWebhook('https://canary.discord.com/api/webhooks/1041692417004408913/9nBnvM_SzeU-3hxgAL0bz411rS1yadS7QxLcfBCUgc37DTR6hCdCl8mm6UeXuqaL3khl', content=goingupmsg)

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                log.exception('Loaded %s', extension)
            except Exception as e:
                log.exception('Falied to load extension %s.', extension)

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                log.exception('In %s:', ctx.command.qualified_name, exc_info=original)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(str(error))

    async def SendWebhook(self, webhookURL: str, content):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhookURL, session=session)
            await webhook.send(content)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = discord.utils.utcnow()
            msgtosend = f'<:check:904229396808888320> Bot is ready <t:{int(time.time())}:F>'
            await self.SendWebhook('https://canary.discord.com/api/webhooks/1041692417004408913/9nBnvM_SzeU-3hxgAL0bz411rS1yadS7QxLcfBCUgc37DTR6hCdCl8mm6UeXuqaL3khl', content=msgtosend)

        log.info('Ready: %s (ID: %s)', self.user, self.user.id)

    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.process_commands(after)

    async def close(self) -> None:
        await super().close()
        await self.session.close()

    async def start(self) -> None:
        await super().start(config("TOKEN"), reconnect=True)


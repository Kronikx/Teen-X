import os
import aiohttp
import asyncio
import discord

from decouple import config
from discord.ext import commands
from ext.functions import sendtologs

os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing underscores

initial_extensions = (
    'jishaku',
    'cogs.admin.owner',
    'cogs.users.information',
    'cogs.unlabled.error_handling'
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
            command_prefix= commands.when_mentioned_or(';'),
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
        self.owner_ids = [168376879479390208, 459439879269646358, 876344421656981544, 948796139954655235]

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                # Send to logs or log to console
                pass

    async def on_message(self, message = discord.Message):
        await self.process_commands(message)

    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.process_commands(after)

    async def on_guild_add(self, guild):
        await sendtologs(self.bot, type='guild', msg=f'Joined guild {guild.name}({guild.id})')

    async def on_guild_remove(self, guild):
        await sendtologs(self.bot, type='guild', msg=f'Left guild {guild.name}({guild.id})')

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def close(self) -> None:
        await super().close()

    async def start(self) -> None:
        await super().start(config("CLEO_TOKEN"), reconnect=True)

async def run_bot():
    async with Slatt() as bot:
        await bot.start()

asyncio.run(run_bot())

import os
import json
import asyncio
import discord

from cogs.owner import Todo
from cogs.embeds import Embeds
from discord.ext import commands

with open('config.json') as config:
    data = json.load(config)

os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing Jishaku underscores

initial_extensions = (
    'cogs.jsk',
    'cogs.owner',
    'cogs.moderation',
    'cogs.information',
    'cogs.error_handling'
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
        self.add_view(Todo())

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                # Send to logs or log to console
                # await loggingEmbed(self, type='error', msg=e)
                pass

    async def on_message(self, message = discord.Message):
        await self.process_commands(message)

    async def on_message_edit(self, before = discord.Message, after = discord.Message):
        if after.embeds or before.embeds:
            return
        if after.author.id == before.author.id:
            return await self.process_commands(after)

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def close(self) -> None:
        await super().close()

    async def start(self) -> None:
        await super().start(data['token'], reconnect=True)

async def run_bot():
    async with Slatt() as bot:
        await bot.start()

asyncio.run(run_bot())

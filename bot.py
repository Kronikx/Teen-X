import os
import asyncio
import time
import contextlib

import discord
import asyncpg

from discord.ext import commands
from decouple import config
from colorama import init, Fore

init(autoreset=True) # Resetting print shit to default
os.environ.setdefault("JISHAKU_HIDE", "1") # Hiding Jishaku from everyone
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1") # Removing underscores
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True)
intentss = discord.Intents(guilds=True, members=True, bans=True, emojis=True, voice_states=False, messages=True, reactions=True, message_content=True)

class Slatt(commands.Bot):
    def __init__(self):
        self.pool_pg = None
        self.token = config("TOKEN")

        self.initial_extensions = [
            'cogs.database',
            'cogs.events',
            'cogs.misc',
            'cogs.owner',
            'cogs.servers']
        super().__init__(
            command_prefix= commands.when_mentioned_or('-'),
            mentions = mentions,
            intents = intentss,
            case_insensitive = True,
            application_id = 1040566823579566160,
            chunk_guilds_at_startup=True,
            heartbeat_timeout=150.0,
            enable_debug_events=True)

    # Starting the bot
    # Do everything here
    async def main(self) -> None:
        """Starts the bot properly"""
        print(f'>> {Fore.MAGENTA}Starting Slatt')
        try:
            start = time.perf_counter()
            print(f'>> {Fore.CYAN}Establishing database connection.....')
            pool_pg = await asyncpg.create_pool(
                host=config('HOST'), database=config('DATABASE'), 
                user=config('USER'), password=config('PWD')
                )
            end = time.perf_counter()
            db_ping = (end - start) * 1000
        except Exception as e:
            print(f'>> {Fore.RED}Couldnt establish DB connection: {e}')
        print(f'>> {Fore.CYAN}Database connection established, ({int(db_ping)}s).')

        async with self, pool_pg:
            self.db = pool_pg
            print(f'>> {Fore.YELLOW}Loading cogs......')
            await self.load_extension('jishaku')
            print(f'  - jishaku')
            for ext in self.initial_extensions:
                await self.load_extension(ext)
                print(f'  - {ext}')
            print(f">> {Fore.GREEN}Finished loading cogs")
            await self.start(self.token)


    async def close(self):
        await super().close()
        await self.db.close()
        print(f'>> {Fore.GREEN}Bot shutdown complete.')


    def starter(self):
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.main())


    async def on_ready(self):
        print(f'>> {Fore.GREEN}Ready: {self.user} (ID: {self.user.id})')


bot = Slatt()
bot.starter()
import sys
import typing
import discord

from discord.ext import commands
from jishaku.features.baseclass import Feature
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES
from jishaku.math import natural_size
from jishaku.modules import package_version

try:
    import psutil
except ImportError:
    psutil = None

try:
    from importlib.metadata import distribution, packages_distributions
except ImportError:
    from importlib_metadata import distribution, packages_distributions  # type: ignore

class CustomJishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    
    @Feature.Command(name="jishaku", aliases=["jsk"], invoke_without_command=True, ignore_extra=False)
    async def jsk(self, ctx: commands.Context):
        """
        The Jishaku debug and diagnostic commands.

        This command on its own gives a status brief.
        All other functionality is within its subcommands.
        """

        # Try to locate what vends the `discord` package
        distributions: typing.List[str] = [
            dist for dist in packages_distributions()['discord']  # type: ignore
            if any(
                file.parts == ('discord', '__init__.py')  # type: ignore
                for file in distribution(dist).files  # type: ignore
            )
        ]

        if distributions:
            dist_version = f'{distributions[0]} `{package_version(distributions[0])}`'
        else:
            dist_version = f'unknown `{discord.__version__}`'

        dev = await self.bot.fetch_user(168376879479390208)

        summary = [
            f"Jishaku v{package_version('jishaku')}, {dist_version}, "
            f"`Python {sys.version[0:6]}` on `{sys.platform}`".replace("\n", ""),
            f"Module was loaded <t:{self.load_time.timestamp():.0f}:R>, "
            f"Cog was loaded <t:{self.start_time.timestamp():.0f}:R>, "
            f"`{len(self.bot.cogs)}/{len(self.bot.cogs)}` Cogs loaded.",
            f"Developed and managed by {dev}",
            ""
        ]

        # detect if [procinfo] feature is installed
        if psutil:
            try:
                proc = psutil.Process()

                with proc.oneshot():
                    try:
                        mem = proc.memory_full_info()
                        summary.append(f"Using {natural_size(mem.rss)} physical memory, "
                                       f"{natural_size(mem.vms)} virtual memory, "
                                       f"{natural_size(mem.uss)} of which unique to this process.")
                    except psutil.AccessDenied:
                        pass

                    try:
                        name = proc.name()
                        pid = proc.pid
                        thread_count = proc.num_threads()

                        summary.append(f"Running on PID {pid} (`{name}`) with {thread_count} thread(s).")
                    except psutil.AccessDenied:
                        pass

                    summary.append("")  # blank line
            except psutil.AccessDenied:
                summary.append(
                    "psutil is installed, but this process does not have high enough access rights "
                    "to query process information."
                )
                summary.append("")  # blank line

        cache_summary = f"{len(self.bot.guilds)} guild(s) and {len(self.bot.users)} user(s)"

        # Show shard settings to summary
        if isinstance(self.bot, discord.AutoShardedClient):
            if len(self.bot.shards) > 20:
                summary.append(
                    f"This bot is automatically sharded ({len(self.bot.shards)} shards of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
            else:
                shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
                summary.append(
                    f"This bot is automatically sharded (Shards {shard_ids} of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
        elif self.bot.shard_count:
            summary.append(
                f"This bot is manually sharded (Shard {self.bot.shard_id} of {self.bot.shard_count})"
                f" and can see {cache_summary}."
            )
        else:
            summary.append(f"This bot is not sharded and can see {cache_summary}.")

        # pylint: disable=protected-access
        if self.bot._connection.max_messages:  # type: ignore
            message_cache = f"Message cache capped at {self.bot._connection.max_messages}"  # type: ignore
        else:
            message_cache = "Message cache is disabled"

        if discord.version_info >= (1, 5, 0):
            remarks = {
                True: 'enabled',
                False: 'disabled',
                None: 'unknown'
            }

            *group, last = (
                f"{intent.replace('_', ' ')} intent is {remarks.get(getattr(self.bot.intents, intent, None))}"
                for intent in
                ('presences', 'members', 'message_content')
            )

            summary.append(f"{message_cache}, {', '.join(group)}, and {last}.")
        else:
            guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"  # type: ignore

            summary.append(f"{message_cache} and {guild_subscriptions}.")

        # pylint: enable=protected-access

        # Show websocket latency in milliseconds
        summary.append(f"Average websocket latency: {round(self.bot.latency * 1000, 2)}ms")

        await ctx.send("\n".join(summary))

async def setup(bot: commands.Bot):
    await bot.add_cog(CustomJishaku(bot=bot))
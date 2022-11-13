import time
import discord

from discord.ext import commands
from utils.functions import sendtologs

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.hybrid_command(name="ping", description='Display the bots ping.', with_app_command=True)
    async def _ping(self, ctx):
        try:
            t_1 = time.perf_counter()
            await ctx.channel.typing() # Getting API ping
            t_2 = time.perf_counter()
            api_ping = round((t_2-t_1)*1000)
        except Exception as e:
            await sendtologs(self, type='error', msg=e)
            pass

        web_ping = round(self.bot.latency*1000) 

        await ctx.reply(f'<a:typing:1040254641121804359> **{api_ping}ms**\n<:discord:1040254738433847317> **{web_ping}ms**')


    # @commands.group(name='emoji', invoke_without_command=False)
    # @commands.has_permissions(manage_emojis=True)
    # @commands.bot_has_permissions(manage_emojis=True)
    # async def _emoji(self, ctx):
    #     pass

    # @_emoji.command(name="add")
    # @commands.has_permissions(manage_emojis=True)
    # @commands.bot_has_permissions(manage_emojis=True)
    # async def _add(self, ctx, emoji: discord.PartialEmoji, *, name = None):
    #     if name == None:
    #         name = emoji.name
    #     else:
    #         name = name.replace(" ", "_")

    #     try:
    #         emote = await emoji.read()
    #         z = await ctx.guild.create_custom_emoji(name=name, image=emote)
    #         await ctx.reply(f'Added {z}')
    #     except Exception as e:
    #         await ctx.reply(f"Error while trying to add emoji, `{e}`")
    #         await sendtologs(self, type='error', msg=e)

    # @_emoji.command(name="delete")
    # @commands.has_permissions(manage_emojis=True)
    # @commands.bot_has_permissions(manage_emojis=True)
    # async def _delete(self, ctx, emoji: discord.Emoji = None):
    #     if emoji == None:
    #         return await ctx.reply("Please provide an emoji")
    #     else:
    #         await emoji.delete()
    #         await ctx.reply(f'`{emoji.name}` deleted!')

    # @_emoji.command(name="rename")
    # @commands.has_permissions(manage_emojis=True)
    # @commands.bot_has_permissions(manage_emojis=True)
    # async def _rename(self, ctx, emoji: discord.Emoji = None, name = None):
    #     if emoji == None or name == None:
    #         await ctx.reply("Invalid arguments.")
    #     else:
    #         await emoji.edit(name=name)
    #         await ctx.reply(f"renamed {emoji}.")


    # @commands.group(name='clear')
    # async def _clear(self, ctx, amount: int):
    #     if amount == None:
    #         await ctx.reply('Please specify an amount of messages to clear.')
    #     elif amount > 1000:
    #         amount = 1000
        
    #     await ctx.message.delete()
    #     await ctx.channel.purge(limit=amount)

    # @_clear.command(name='after')
    # async def _after(self, ctx, after):
    #     await ctx.message.delete()
    #     async for message in ctx.channel.history(after=after):
    #         await message.delete()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Misc(bot),
        guilds = [discord.Object(id = 1037005626112491522), discord.Object(id = 924924186697281567)])
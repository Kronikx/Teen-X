import discord

from discord.ext import commands

async def loggingEmbed(self, type: str, msg: str):

    error_channel = self.get_channel(1043940794450595897)
    guild_channel = self.get_channel(1043940794450595896)

    embed = discord.Embed(color=0xff0000)

    if format == "error":
        embed.add_field(name="Error", value=f"```py\n{msg}\n```")
        await error_channel.send(embed=embed)
    elif format == "guild":
        embed.add_field(name="Guilds", value=f"```\n{msg}\n```")
        await guild_channel.send(embed=embed)

class Embeds():
    def success(self, msg: str):
        embed = discord.Embed(description=f"✅: {msg}", color=discord.Color.green())
        return embed

    def unhandled(self):
        embed = discord.Embed(description=f"⚠️: An unexpected error has occured. My developers have been notified.", color=discord.Color.yellow())
        return embed

    def error(self, error_msg: str):
        embed = discord.Embed(description=f"❌: {error_msg}", color=discord.Color.red())
        return embed
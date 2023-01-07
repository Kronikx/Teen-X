import discord

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
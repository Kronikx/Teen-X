import discord

async def sendtologs(self, type, msg):
    error_channel = self.bot.get_channel(1037010318544617554)
    guild_channel = self.bot.get_channel(1040221622826700843)
    database_channel = self.bot.get_channel(1040223211012501565)

    if type == "error":
        eem = discord.Embed(color=0xff0000)
        eem.add_field(name="Error", value=f"```py\n{msg}\n```")
        await error_channel.send(embed=eem)
    elif type == "guild":
        gem = discord.Embed(color=0x800080)
        gem.add_field(name="Guilds", value=f"```\n{msg}\n```")
        await guild_channel.send(embed=gem)
    elif type == "database":
        dem = discord.Embed(color=0xffc0cb)
        dem.add_field(name="Database", value=f"```\n{msg}\n```")
        await database_channel.send(embed=dem)
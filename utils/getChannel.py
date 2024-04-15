def getChannel(channelID: int, guildID: int, bot):
    guild = bot.get_guild(guildID)
    if guild and channelID is not None:
        return guild.get_channel(channelID)

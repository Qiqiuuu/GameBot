import discord
from discord import app_commands
from discord.ext import commands
import json


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channelsData = {}

    @app_commands.command(name='setcasinochannel', description="Set this channel for your Casino!")
    async def setCasino(self, interaction: discord.Interaction):
        data = self.getData()
        for entry in data["guilds"]:
            if entry["guildID"] == interaction.guild.id:
                entry["casinoChannel"] = interaction.channel.id
                break

        with open('casinoChannels.json', 'w') as file:
            json.dump(data, file, indent=4)

        self.syncChannels()

    def checkGuild(self, guild: discord.Guild):
        data = self.getData()
        for entry in data["guilds"]:
            if entry["guildID"] == guild.id:
                return
        data["guilds"].append({"guildID": guild.id, "casinoChannel": None})
        with open('casinoChannels.json', 'w') as file:
            json.dump(data, file, indent=4)

    def syncChannels(self):
        print("syncing channels")
        data = self.getData()
        for entry in data["guilds"]:
            self.channelsData.update({entry["guildID"]: entry["casinoChannel"]})

    async def clearChannels(self):
        for guild_id, channel_id in self.channelsData.items():
            guild = self.bot.get_guild(int(guild_id))
            if guild and channel_id is not None:
                channel = guild.get_channel(int(channel_id))
                if channel:
                    await channel.purge()
        print("Channels purged")

    def getData(self):
        try:
            with open('casinoChannels.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Couldn't open casinoChannels file")


async def setup(bot):
    await bot.add_cog(Casino(bot))

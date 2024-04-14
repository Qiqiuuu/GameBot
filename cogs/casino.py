import discord
from discord import app_commands
from discord.ext import commands
import json
from discord.components import SelectMenu

from utils.interactionRespond import interactionRespond
from utils.getChannel import getChannel


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channelsData = {}

    @app_commands.command(name='setcasinochannel', description="Set this channel for your Casino!")
    async def setCasino(self, interaction: discord.Interaction):
        data = self.getData()
        for guildID, channelID in self.channelsData.items():
            if guildID == interaction.guild.id:
                channelID = interaction.channel.id
                data["casinoChannel"] = channelID
                break

        with open('casinoChannels.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.syncChannels()
        interaction.response.send_message("Casino is set")
        await interactionRespond(interaction)

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
        for guildID, channelID in self.channelsData.items():
            channel = getChannel(channelID,guildID,self.bot)
            if channel:
                await channel.purge()
        print("Channels purged")

    def getData(self):
        try:
            with open('casinoChannels.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Couldn't open casinoChannels file")


    def casinoMenu(self):
        for guildID, channelID in self.channelsData.items():
            channel = getChannel(channelID, guildID, self.bot)
            if channel:
                channel.send




async def setup(bot):
    await bot.add_cog(Casino(bot))

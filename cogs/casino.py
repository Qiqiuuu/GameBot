import discord
from discord import app_commands
from discord.ext import commands
import json
from discord.components import SelectMenu

from utils.interactionRespond import interactionRespond
from utils.interactionUserMember import interactionUserMember
from utils.getChannel import getChannel
from cogs.helpClasses.casinoView import CasinoView
from cogs.helpClasses.embed import Embed
from cogs.helpClasses.blackjackView import BlackJackView
from cogs.blackJack import BlackJack


class Casino(commands.Cog):
    def __init__(self, bot):
        self.messageBlackJackID = {}
        self.bot = bot
        self.channelsData = {}
        self.playingUsers = {}
        self.startingLobby = {}
        self.embed = Embed()
        self.messageCasinoMenuID = {}
        self.casinoView = CasinoView(self.bot, self)
        self.blackjackView = BlackJackView(self.bot)

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

    async def afterInit(self):
        self.syncChannels()
        await self.clearChannels()
        await self.casinoMenu()
        await self.blackJack()

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
            self.playingUsers.update({entry["guildID"]: {}})
            self.startingLobby.update({entry["guildID"]: {}})

    async def clearChannels(self):
        for guildID, channelID in self.channelsData.items():
            channel = getChannel(channelID, guildID, self.bot)
            if channel:
                await channel.purge()
        print("Channels purged")

    def getData(self):
        try:
            with open('casinoChannels.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Couldn't open casinoChannels file")

    async def casinoMenu(self):
        for guildID, channelID in self.channelsData.items():
            channel = getChannel(channelID, guildID, self.bot)
            games = self.casinoView.getGames()
            for guild in self.playingUsers:
                for game in games:
                    if game not in self.playingUsers[guild]:
                        self.playingUsers[guild].update({game: []})
                        self.startingLobby[guild].update({game: False})
            if channel:
                mID = await channel.send(view=self.casinoView,
                                         embeds=[self.embed.casinoWelcome(),
                                                 self.embed.casinoLobby(self.playingUsers[guildID])])
                self.messageCasinoMenuID.update({guildID: mID})

    async def blackJack(self):
        for guildID, channelID in self.channelsData.items():
            channel = getChannel(channelID, guildID, self.bot)
            games = self.casinoView.getGames()
            for guild in self.playingUsers:
                for game in games:
                    if game not in self.playingUsers[guild]:
                        self.playingUsers[guild].update({game: []})
            if channel:
                mID = await channel.send(embed=self.embed.waitingBlackJack())
                self.messageBlackJackID.update({guildID: mID})

    async def blackJackGame(self, interaction: discord.Interaction):
        message = self.messageBlackJackID[interaction.guild.id]
        if self.playingUsers[message.guild.id]["Black Jack"] and self.startingLobby[message.guild.id][
            "Black Jack"] == False:
            self.startingLobby[message.guild.id]["Black Jack"] = True
            # oczekiwanie np 20 sec i zobacz czy sa ludzie w lobby zaraz przed
            if not self.playingUsers[message.guild.id]["Black Jack"]:
                await message.edit(embed=self.embed.waitingBlackJack(), view=None)
                return
            BJ = BlackJack(self.bot, message.channel.id, self.playingUsers[message.guild.id]["Black Jack"])
            await BJ.blackJackMain(message)
            BJResults = BJ.retResults()
            self.startingLobby[message.guild.id]["Black Jack"] = False
            if self.playingUsers[message.guild.id]["Black Jack"]:
                await self.blackJackGame(message)
            else:
                await message.edit(embed=self.embed.waitingBlackJack(), view=None)

    def addPlayer(self, interaction: discord.Interaction, game: str):
        guild = self.playingUsers[interaction.guild.id]
        interactionUser = interactionUserMember(interaction)
        if interactionUser not in guild[game]:
            guild[game].append(interactionUser)
        else:
            return False

    def removePlayer(self, interaction: discord.Interaction, game: str):
        guild = self.playingUsers[interaction.guild.id]
        interactionUser = interactionUserMember(interaction)
        if interactionUser in guild[game]:
            guild[game].remove(interactionUser)
        else:
            return False

    def getPlayers(self, interaction: discord.Interaction):
        guild = self.playingUsers[interaction.guild.id]
        return guild

    async def refreshMenuMessage(self, guildID):
        if guildID in self.messageCasinoMenuID:
            channelID = self.channelsData[guildID]
            channel = self.bot.get_channel(channelID)
            messageID = self.messageCasinoMenuID[guildID]
            message = await channel.fetch_message(messageID.id)
            await message.edit(view=self.casinoView,
                               embeds=[self.embed.casinoWelcome(), self.embed.casinoLobby(self.playingUsers[guildID])])


async def setup(bot):
    await bot.add_cog(Casino(bot))

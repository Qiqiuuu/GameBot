import random
import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.lobby import Lobby
from cogs.helpClasses.embed import Embed
from cogs.helpClasses.rouletteView import RouletteView
from bot import GameBot


class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.playerList = None
        self.interaction = None
        self.bot = bot
        self.embed = Embed()
        self.emoji = ['😀', '😏', '😎', '😜', '😱', '🤡', '🤠', '🎃']
        self.playerStatus = None
        self.result = None
        self.gameID = 1225538557171470348

    @app_commands.command(name='russianroulette', description='Let roulette spin!')
    async def russianRoulette(self, interaction: discord.Interaction, bet: int = 0):
        lobby = Lobby(self.bot, "Russian Roulette", bet)
        await lobby.creatingLobby(interaction)
        self.playerList, self.interaction, self.result = await lobby.returnList()

        await asyncio.sleep(2)
        if self.result:
            rouletteView = RouletteView(interaction, self.playerList, self, bet)
            self.playerStatus = self.assignStatus()

            await self.interaction.edit_original_response(embed=self.embed.rouletteStart(self.playerStatus),
                                                          view=rouletteView)
            winner, losers = await rouletteView.returnResults()
            self.bot.getdataBase().addWin(winner, self.gameID, bet * len(losers))
            for member in losers:
                self.bot.getdataBase().addLose(member, self.gameID, bet)

            await self.interaction.edit_original_response(embed=self.embed.rouletteEnd(winner, (bet * len(losers))),
                                                          view=None)

    def assignStatus(self):
        status = {}
        for player in self.playerList:
            status[player] = random.choice(self.emoji)
        return status

    def roulette(self):
        for player in self.playerStatus:
            if 0 == random.randint(0, 6):
                self.playerStatus[player] = '💀'
                return [True, player]
        return [False, None]

    def checkAlivePlayers(self):
        alivePlayers = {player: emoji for player, emoji in self.playerStatus.items() if emoji != '💀'}
        return [True if len(alivePlayers) == 1 else False, alivePlayers]

    def getPlayerStatus(self):
        return self.playerStatus


async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))

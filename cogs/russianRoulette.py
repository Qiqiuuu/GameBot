import random
import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from GameBot.cogs.helpClasses.lobby import Lobby
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.cogs.helpClasses.buttonsRoulette import ButtonsRoulette


class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.playerList = None
        self.interaction = None
        self.bot = bot
        self.embed = Embed()
        self.emoji = ['😀', '😏', '😎', '😜', '😱', '🤡', '🤠', '🎃']
        self.playerStatus = None

    @app_commands.command(name='russianroulette', description='Let roulette spin!')
    async def russianRoulette(self, interaction: discord.Interaction):
        lobby = Lobby(self.bot, "Russian Roulette")
        await lobby.creatingLobby(interaction)
        self.playerList, self.interaction, = await lobby.returnList()

        await asyncio.sleep(2)

        rouletteView = ButtonsRoulette(interaction, self.playerList, self)
        self.playerStatus = self.assignStatus()

        await self.interaction.edit_original_response(embed=self.embed.rouletteStart(self.playerStatus),
                                                      view=rouletteView)
        winner = await rouletteView.returnWinner()
        await self.interaction.edit_original_response(embed=self.embed.rouletteEnd(winner),
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

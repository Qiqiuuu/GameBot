import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.embed import Embed
from cogs.helpClasses.cards import Cards
from cogs.helpClasses.blackjackGameView import BlackJackGameView
from utils.interactionUserMember import interactionUserMember


class BlackJack(commands.Cog):
    def __init__(self, bot, channelID: int, playersList: dict):
        self.playersCards = None
        self.MID = None
        self.bot = bot
        self.embed = Embed()
        self.deck = Cards()
        self.playersList = playersList
        self.channelID = channelID
        self.croupierFirstCard = None
        self.canPlay = dict.fromkeys(self.playersList, False)

    async def blackJackMain(self, channelID: int):
        self.setPlayerCards()
        channel = self.bot.get_channel(channelID)
        if channel:
            self.MID = await channel.send(
                view=BlackJackGameView(self.bot, self),
                embeds=[self.embed.blackjackHelp(), self.embed.mainBlackJack(self.playersCards)])
            await self.deal()





    async def deal(self):
        self.croupierFirstCard = self.deck.takeCard()
        self.playersCards['croupier'].append('X')
        await asyncio.sleep(0.25)
        await self.MID.edit(view=BlackJackGameView(self.bot, self),
                            embeds=[self.embed.blackjackHelp(),
                                    self.embed.mainBlackJack(self.playersCards)])
        self.playersCards['croupier'].append(self.deck.takeCard())
        await asyncio.sleep(0.25)
        await self.MID.edit(view=BlackJackGameView(self.bot, self),
                            embeds=[self.embed.blackjackHelp(),
                                    self.embed.mainBlackJack(self.playersCards)])
        for _ in range(2):
            for player, cards in self.playersCards.items():
                if player != 'croupier':
                    cards.append(self.deck.takeCard())
                    await asyncio.sleep(0.25)
                    await self.MID.edit(view=BlackJackGameView(self.bot, self),
                                        embeds=[self.embed.blackjackHelp(),
                                                self.embed.mainBlackJack(self.playersCards)])


    async def updateCards(self, interaction: discord.Interaction):
        interactionUser = interactionUserMember(interaction)
        if interactionUser.id in self.playersList:
            self.playersCards[interactionUser].append(self.deck.takeCard())
            await asyncio.sleep(0.25)
            await interaction.edit_original_response(view=BlackJackGameView(self.bot),
                                                     embeds=[self.embed.blackjackHelp(),
                                                             self.
                                                     embed.mainBlackJack(self.playersCards)])

    def retMID(self):
        return self.MID


    def updatePlayersList(self, playersList):
        self.playersList = playersList

    def setPlayerCards(self):
        self.playersCards = {'croupier': []}
        for player in self.playersList:
            self.playersCards[player] = []

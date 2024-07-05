import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.embed import Embed
from cogs.helpClasses.cards import Cards
from cogs.helpClasses.blackjackGameView import BlackJackGameView
from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond


class BlackJack(commands.Cog):
    def __init__(self, bot, channelID: int, playersList: dict):
        self.croupierResult = None
        self.playersCards = None
        self.MID = None
        self.bot = bot
        self.embed = Embed()
        self.deck = Cards()
        self.playersList = playersList
        self.channelID = channelID
        self.croupierFirstCard = None
        self.canPlay = dict.fromkeys(self.playersList, False)
        self.results = dict.fromkeys(self.playersList, "")

    async def blackJackMain(self, message):
        self.setPlayerCards()
        channel = self.bot.get_channel(message.channel.id)
        if channel:
            self.MID = await message.edit(
                view=BlackJackGameView(self.bot, self),
                embeds=[self.embed.blackjackHelp(), self.embed.mainBlackJack(self.playersCards)])
            await self.deal()
            await self.waitForPlayersOrTimeout(30)
            await self.croupierHit()
            self.checkResults()
            await asyncio.sleep(0.5)
            self.MID = await message.edit(
                view=BlackJackGameView(self.bot, self),
                embeds=[self.embed.blackjackHelp(), self.embed.mainBlackJack(self.playersCards)])


    async def croupierHit(self):
        self.playersCards['croupier'][0] = self.croupierFirstCard
        await asyncio.sleep(0.75)
        await self.MID.edit(view=BlackJackGameView(self.bot, self),
                            embeds=[self.embed.blackjackHelp(),
                                    self.embed.mainBlackJack(self.playersCards)])
        while self.cardsSum("croupier") <= 17:
            self.playersCards['croupier'].append(self.deck.takeCard())
            await asyncio.sleep(0.75)
            await self.MID.edit(view=BlackJackGameView(self.bot, self),
                                embeds=[self.embed.blackjackHelp(),
                                        self.embed.mainBlackJack(self.playersCards)])
        self.croupierResult = self.cardsSum("croupier")

    async def deal(self):
        self.croupierFirstCard = self.deck.takeCard()
        self.playersCards['croupier'].append('X')
        await asyncio.sleep(0.75)
        await self.MID.edit(view=BlackJackGameView(self.bot, self),
                            embeds=[self.embed.blackjackHelp(),
                                    self.embed.mainBlackJack(self.playersCards)])
        self.playersCards['croupier'].append(self.deck.takeCard())
        await asyncio.sleep(0.75)
        await self.MID.edit(view=BlackJackGameView(self.bot, self),
                            embeds=[self.embed.blackjackHelp(),
                                    self.embed.mainBlackJack(self.playersCards)])
        for _ in range(2):
            for player, cards in self.playersCards.items():
                if player != 'croupier':
                    cards.append(self.deck.takeCard())
                    await asyncio.sleep(0.75)
                    await self.MID.edit(view=BlackJackGameView(self.bot, self),
                                        embeds=[self.embed.blackjackHelp(),
                                                self.embed.mainBlackJack(self.playersCards)])
                    if self.checkCards(player):
                        await asyncio.sleep(0.25)
                        await self.MID.edit(view=BlackJackGameView(self.bot,self),
                                            embeds=[self.embed.blackjackHelp(),
                                                    self.embed.mainBlackJack(self.playersCards)])

    async def updateCards(self, interaction: discord.Interaction):
        interactionUser = interactionUserMember(interaction)
        if interactionUser.id in self.playersList:
            self.playersCards[interactionUser].append(self.deck.takeCard())
            await asyncio.sleep(0.75)
            await interaction.edit_original_response(view=BlackJackGameView(self.bot),
                                                     embeds=[self.embed.blackjackHelp(),
                                                             self.
                                                     embed.mainBlackJack(self.playersCards)])
            if self.checkCards(interactionUser):
                await asyncio.sleep(0.75)
                await interaction.edit_original_response(view=BlackJackGameView(self.bot),
                                                         embeds=[self.embed.blackjackHelp(),
                                                                 self.
                                                         embed.mainBlackJack(self.playersCards)])
        interactionRespond(interaction)

    def checkResults(self):
        for player in self.playersCards:
            if self.cardsSum(player) >= self.croupierResult and self.cardsSum(player) > 21:
                self.results[player] = "Lost"
            else:
                self.playersCards[player] = ["You Won"]
                self.results[player] = "Won"

    async def waitForPlayersOrTimeout(self, timeoutSecs: int):
        try:
            await asyncio.wait_for(self.waitForPlayers(), timeout=timeoutSecs)
            return True
        except asyncio.TimeoutError:
            return False

    async def waitForPlayers(self):
        while not self.canPlay:
            await asyncio.sleep(1)

    def checkCards(self, member: discord.Member):
        if self.cardsSum(member) > 21:
            self.canPlay[member] = True
            self.playersCards[member] = ["You Lost"]
            self.results[member] = "Lost"
            return True
        return False

    def cardsSum(self, member):
        sumOfCards = 0
        cardValue = {'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        for card in self.playersCards[member]:
            if card in cardValue:
                sumOfCards += cardValue[card]
            else:
                sumOfCards += int(card)
        return sumOfCards

    def retMID(self):
        return self.MID

    def retCanPlay(self):
        return self.canPlay
    def retResults(self):
        return self.results

    def setTrueCanPlay(self, member: discord.Member):
        self.canPlay[member] = True

    def updatePlayersList(self, playersList):
        self.playersList = playersList

    def setPlayerCards(self):
        self.playersCards = {'croupier': []}
        for player in self.playersList:
            self.playersCards[player] = []

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.embed import Embed
from cogs.helpClasses.card import Card

class BlackJack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.deck = Card().createCardDeck()



    def setBlackJack(self, channelID: int):
        channel = self.bot.get_channel(channelID)
        if channel:
            await channel.send("XDDD")





import random
from enum import Enum


class Cards():
    def __init__(self):
        self.deck = None
        self.createCardDeck()

    def createCardDeck(self):
        rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = rank * 4

    def takeCard(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

import random
from enum import Enum


class Cards(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11

    def __init__(self):
        self.deck = None

    def createCardDeck(self):
        self.deck = [rank for rank in Cards for _ in range(4)]

    def takeCard(self):
        card = random.sample(self.deck, 1)
        self.deck.remove(card)
        return card

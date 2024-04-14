import discord

from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond

class BlackJackView(discord.ui.View):
    def __init__(self):
        super().__init__()

    # @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    # async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    # @discord.ui.button(label='Stand', style=discord.ButtonStyle.blurple)
    # async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    # @discord.ui.button(label='+5', style=discord.ButtonStyle.blurple)
    # async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    # @discord.ui.button(label='+10', style=discord.ButtonStyle.blurple)
    # async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):


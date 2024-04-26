import discord

from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond

class BlackJackGameView(discord.ui.View):
    def __init__(self, bot, blackJack):
        super().__init__()
        self.bot = bot
        self.blackJack = blackJack

    @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        return False
    @discord.ui.button(label='Stand', style=discord.ButtonStyle.blurple)
    async def gmButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        return False


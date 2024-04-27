import discord

from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond


class BlackJackGameView(discord.ui.View):
    def __init__(self, bot, blackJack):
        super().__init__()
        self.bot = bot
        self.blackJack = blackJack

    @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    async def hitButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        if interactionUser in self.blackJack.canPlay() and self.blackJack.canPlay()[interactionUser] == False:
            self.blackJack.updateCards(interaction)
        interactionRespond(interaction)

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.blurple)
    async def standButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        if interactionUser in self.blackJack.canPlay():
            self.blackJack.canPlay()[interactionUser] = True
        interactionRespond(interaction)

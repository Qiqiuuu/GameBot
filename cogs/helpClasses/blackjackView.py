import discord

from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond


class BlackJackView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label='+5', style=discord.ButtonStyle.blurple)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        return False

    @discord.ui.button(label='+10', style=discord.ButtonStyle.blurple)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        return False

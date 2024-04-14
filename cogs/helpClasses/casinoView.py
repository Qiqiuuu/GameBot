import discord.ui
from cogs.helpClasses.casinoMenu import CasinoMenu
from utils.interactionUserMember import interactionUserMember


class CasinoView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.casino = CasinoMenu()

    @discord.ui.Button(label="Join", style=discord.ButtonStyle.green)
    async def joinButton(self, interaction: discord.Interaction):
        interactionUser = interactionUserMember(interaction)
        return interactionUser

    @discord.ui.Button(label="Leave", style=discord.ButtonStyle.red)
    async def leaveButton(self, interaction: discord.Interaction):
        interactionUser = interactionUserMember(interaction)
        return interactionUser

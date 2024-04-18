import discord.ui
from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond


class CasinoView(discord.ui.View):
    def __init__(self, bot, casino):
        super().__init__()
        self.bot = bot
        self.casino = casino

    @discord.ui.select(placeholder='Select a game', options=[
        discord.SelectOption(label="Black Jack", description="Join/Leave Black Jack"),
        discord.SelectOption(label="Roulette", description="Join/Leave Roulette")
    ])
    async def select_game(self, interaction: discord.Interaction, select: discord.ui.Select):
        interactionUser = interactionUserMember(interaction)

        pass

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def joinButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        self.casino.addPlayer(interaction)
        self.casino.getPlayers(interaction)
        await interactionRespond(interaction)
        return interactionUser

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
    async def leaveButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        print(interactionUser)
        await interactionRespond(interaction)
        return interactionUser

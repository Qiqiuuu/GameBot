import discord.ui
from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond


class CasinoView(discord.ui.View):
    def __init__(self, bot, casino):
        super().__init__(timeout=None)
        self.bot = bot
        self.casino = casino
        self.currentOption = None
        self.games = ["Black Jack", "Roulette"]

    @discord.ui.select(placeholder='Select a game', options=[
        discord.SelectOption(label="Black Jack", description="Join/Leave Black Jack"),
        discord.SelectOption(label="Roulette", description="Join/Leave Roulette")
    ])
    async def selectGame(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.currentOption = select.values[0]
        await interactionRespond(interaction)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def joinButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentOption is not None:
            print(self.currentOption)
            if self.currentOption == "Black Jack":
                self.casino.addPlayer(interaction, self.currentOption)
                await self.casino.blackJackGame(interaction.message)
        await self.casino.refreshMenuMessage(interaction.guild.id)
        await interactionRespond(interaction)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
    async def leaveButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentOption is not None:
            self.casino.removePlayer(interaction, self.currentOption)
        await self.casino.refreshMenuMessage(interaction.guild.id)
        await interactionRespond(interaction)

    def getGames(self):
        return self.games

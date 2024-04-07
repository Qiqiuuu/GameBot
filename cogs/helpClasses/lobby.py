import discord
from cogs.helpClasses.embed import Embed
from utils.interactionUserMember import interactionUserMember
from utils.interactionRespond import interactionRespond
from bot import GameBot


class Lobby(discord.ui.View):
    def __init__(self, bot, gameName: str, bet: int):
        super().__init__()
        self.interaction = None
        self.bot = bot
        self.gameName = gameName
        self.bet = bet
        self.playersList = []
        self.embed = Embed()
        self.dataBase = self.bot.getdataBase()
        self.result = None

    def getEmbed(self):
        return self.embed.startLobby(self.gameName, self.playersList, self.bet)

    async def creatingLobby(self, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.send_message(embed=self.getEmbed(),
                                                view=self)

    @discord.ui.button(label='Add to Lobby', style=discord.ButtonStyle.blurple)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        if interactionUser not in self.playersList:
            if self.dataBase.getCoins(interactionUser) > self.bet:
                self.addPlayer(interactionUser)
                await self.interaction.edit_original_response(embed=self.getEmbed())
            else:
                await interaction.response.send_message(content=f"You don't have enough coins for this lobby!",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(content=f"You already joind lobby!",
                                                    ephemeral=True)
        await interactionRespond(self.interaction)
        await interactionRespond(interaction)

    @discord.ui.button(label="Close Lobby", style=discord.ButtonStyle.green)
    async def closeButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.interaction.user.id:
            if len(self.playersList) == 0:
                await interaction.response.send_message(content=f"Can't close an empty lobby!",
                                                        ephemeral=True)
            else:
                await self.interaction.edit_original_response(
                    embed=self.embed.closingLobby(self.gameName, self.playersList),
                    view=None)
                self.result = True
                self.stop()
        else:
            await interaction.response.send_message(content=f"Only host can close lobby",
                                                    ephemeral=True)
        await interactionRespond(self.interaction)
        await interactionRespond(interaction)

    @discord.ui.button(label="Cancel Lobby", style=discord.ButtonStyle.red)
    async def cancelButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.interaction.user.id:
            await self.interaction.edit_original_response(embed=self.embed.cancelLobby(self.gameName),
                                                          view=None)
            self.result = False
            self.stop()
        else:
            await interaction.response.send_message(content=f"Only host can cancel lobby",
                                                    ephemeral=True)
        await interactionRespond(self.interaction)
        await interactionRespond(interaction)

    def addPlayer(self, player):
        self.playersList.append(player)

    async def returnList(self):
        await self.wait()
        return [self.playersList, self.interaction, self.result]

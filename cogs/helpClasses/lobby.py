import discord
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.utils.interactionUserMember import interactionUserMember
from GameBot.utils.interactionRespond import interactionRespond


class Lobby(discord.ui.View):
    def __init__(self, bot, gameName: str):
        super().__init__()
        self.interaction = None
        self.bot = bot
        self.gameName = gameName
        self.playersList = []
        self.embed = Embed()

    def getEmbed(self):
        return self.embed.startLobby(self.gameName, self.playersList)

    async def creatingLobby(self, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.send_message(embed=self.getEmbed(),
                                                view=self)

    @discord.ui.button(label='Add to Lobby', style=discord.ButtonStyle.green)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        if interactionUser not in self.playersList:
            self.addPlayer(interactionUser)
            await self.interaction.edit_original_response(embed=self.getEmbed())
        else:
            await interaction.response.send_message(content=f"You already joind lobby!",
                                                    ephemeral=True)
        await interactionRespond(self.interaction)
        await interactionRespond(interaction)

    @discord.ui.button(label="Close Lobby",style=discord.ButtonStyle.red)
    async def closeButton(self,interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.interaction.user.id:
            await self.interaction.edit_original_response(embed=self.embed.closingLobby(self.gameName, self.playersList),
                                                    view = None)
            self.stop()
        else:
            await interaction.response.send_message(content=f"You can't close lobby!",
                                                    ephemeral=True)
        await interactionRespond(self.interaction)
        await interactionRespond(interaction)

    def addPlayer(self, player):
        self.playersList.append(player)

    async def returnList(self):
        await self.wait()
        return [self.playersList,self.interaction]



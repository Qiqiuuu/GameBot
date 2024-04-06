import discord
from GameBot.utils.interactionUserMember import interactionUserMember
from GameBot.utils.interactionRespond import interactionRespond
from GameBot.cogs.helpClasses.embed import Embed


class ButtonsRoulette(discord.ui.View):
    def __init__(self, interaction, playerList, russianRoulette):
        super().__init__()
        self.russianRoulette = russianRoulette
        self.winner = None
        self.interaction = interaction
        self.playerList = playerList
        self.embed = Embed()

    @discord.ui.button(label='Next Round 🔫', style=discord.ButtonStyle.grey)
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        if interactionUser in self.playerList:
            isWinner, alivePlayers = self.russianRoulette.checkAlivePlayers()
            if isWinner:
                self.winner = list(alivePlayers.keys())[0]
                self.stop()
            else:
                isDead, deadPlayer = self.russianRoulette.roulette()
                if isDead:
                    await self.interaction.edit_original_response(
                        embed=self.embed.rouletteDied(deadPlayer, self.russianRoulette.getPlayerStatus()))
                else:
                    await self.interaction.edit_original_response(
                        embed=self.embed.rouletteSurvived(self.russianRoulette.getPlayerStatus()))
        else:
            await interaction.response.send_message(content=f"You are not playing!",
                                                    ephemeral=True)
        await interactionRespond(interaction)
        await interactionRespond(self.interaction)

    async def returnResults(self):
        await self.wait()
        return [self.winner,self.playerList.remove(self.winner)]

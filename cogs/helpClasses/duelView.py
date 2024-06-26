import discord
from utils.interactionRespond import interactionRespond


# duel class
class DuelView(discord.ui.View):
    def __init__(self, challengingUser, challengedUser, bot):
        super().__init__()
        self.bot = bot
        self.value = None
        self.challengingUser = challengingUser
        self.challengedUser = challengedUser
        self.buttonPressed = None

    # main button handler
    async def handleButton(self, interaction: discord.Interaction, button: discord.ui.Button, label: str,
                           accepted: bool):
        if interaction.user.id == self.challengedUser.id:
            button.disabled = True
            button.label = label
            self.buttonPressed = accepted
            button.style = discord.ButtonStyle.grey
            if interaction.message:
                await interaction.message.edit(view=self)
            self.stop()
        else:
            await interaction.response.send_message('You are not the challenged user!', ephemeral=True)
        await interactionRespond(interaction)

    # buttons for accpeting/declining duel
    @discord.ui.button(label='Accept Duel', style=discord.ButtonStyle.green)
    async def acceptButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handleButton(interaction, button, 'Duel Accepted', True)

    @discord.ui.button(label='Decline Duel', style=discord.ButtonStyle.red)
    async def declineButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handleButton(interaction, button, 'Duel Rejected', False)

    # return pressed button
    async def getButtonPressed(self):
        await self.wait()
        return self.buttonPressed

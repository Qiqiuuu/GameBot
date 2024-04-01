import discord

class DuelView(discord.ui.View):
  def __init__(self,bot,challenged,challenger):
      super().__init__()
      self.bot = bot
      self.value = None
      self.challenger = challenger
      self.challenged = challenged
      self.buttonPressed = None
    
  async def handle_button(self, interaction: discord.Interaction, button: discord.ui.Button, label: str, accepted: bool):
    if interaction.user.id == self.challenged.id:
      button.disabled = True
      button.label = label
      self.buttonPressed = accepted
      button.style = discord.ButtonStyle.grey
      if interaction.message:
          await interaction.message.edit(view=self)
      self.stop()
    else:
      await interaction.response.send_message('You are not the challenged user!', ephemeral=True)
    await interaction.response.defer()

  @discord.ui.button(label='Accept Duel', style=discord.ButtonStyle.green)
  async def acceptButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_button(interaction, button, 'Duel Accepted', True)

  @discord.ui.button(label='Decline Duel', style=discord.ButtonStyle.red)
  async def declineButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_button(interaction, button, 'Duel Rejected', False)

  def getButtonPressed(self):
    return self.buttonPressed

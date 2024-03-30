import discord

from cogs.helpClasses.duelDm import duelDm


class duelView(discord.ui.View):
  def __init__(self,bot,challenged,challenger):
      super().__init__()
      self.bot = bot
      self.value = None
      self.challenger = challenger
      self.challenged = challenged
    
    

  @discord.ui.button(label='Accept Duel',style=discord.ButtonStyle.green)
  async def acceptButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    if interaction.user.id == self.challenged.id:
      button.disabled = True
      button.label = 'Duel Accepted'
      button.style = discord.ButtonStyle.grey
      if interaction.message:
        await interaction.message.edit(view=self)
      return button.label
      
    else:
      await interaction.response.send_message('You are not the challenged user!', ephemeral=True)

  @discord.ui.button(label='Decline Duel',style=discord.ButtonStyle.red)
  async def declineButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    if interaction.user.id == self.challenged.id:
      button.disabled = True
      button.label = 'Duel Rejected'
      button.style = discord.ButtonStyle.grey
      if interaction.message:
        await interaction.message.edit(view=self)
      return button.label
    else:
      await interaction.response.send_message('You are not the challenged user!', ephemeral=True)



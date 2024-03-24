import discord
from discord import emoji


class dmView(discord.ui.View):
  def __init__(self, challengedUser):
      super().__init__()
      self.value = None
      self.challengedUserId = challengedUser.id
      self.chosenHand = None


  @discord.ui.button(label='Rock',style=discord.ButtonStyle.blurple, emoji = '🗿')
  async def rockButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.chosenHand = "rock"
    button.disabled = True
    button.style = discord.ButtonStyle.grey
    if interaction.message:
      await interaction.message.edit(view=self)
    self.stop()

  @discord.ui.button(label='Paper',style=discord.ButtonStyle.blurple, emoji = '📄')
  async def paperButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.chosenHand = "paper"
    button.disabled = True
    button.style = discord.ButtonStyle.grey
    if interaction.message:
      await interaction.message.edit(view=self)
    self.stop()

  @discord.ui.button(label='Scissors',style=discord.ButtonStyle.blurple, emoji = '✂️')
  async def scissorsButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.chosenHand = "scissors"
    button.disabled = True
    button.style = discord.ButtonStyle.grey
    if interaction.message:
      await interaction.message.edit(view=self)
    self.stop()

  async def getHand(self):
    return self.chosenHand

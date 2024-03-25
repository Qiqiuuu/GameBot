import discord
from discord import emoji
import asyncio

from discord import interactions


class dmView(discord.ui.View):
  def __init__(self, challengedUser,bot):
      super().__init__()
      self.bot = bot
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
    try:
      await self.bot.wait_for('interaction', timeout=30,check = self.interaction_check)
      print(self.chosenHand)
      return self.chosenHand
    except asyncio.TimeoutError:
      return "Timed Out"
    

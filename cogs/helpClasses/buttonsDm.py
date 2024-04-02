import discord

class DmView(discord.ui.View):
  def __init__(self, challengedUser, bot):
      super().__init__()
      self.bot = bot
      self.value = None
      self.challengedUserId = challengedUser.id
      self.chosenHand = None

  async def button(self, hand: str, interaction: discord.Interaction, button: discord.ui.Button):
      try:
          self.chosenHand = hand
          button.disabled = True
          button.style = discord.ButtonStyle.grey
          if interaction.message:
              await interaction.message.edit(view=self)
          self.stop()
      except Exception as e:
          print(f"Error handling {hand} button click: {e}")
      await interaction.response.defer()

  @discord.ui.button(label='Rock', style=discord.ButtonStyle.blurple, emoji='🗿')
  async def rockButton(self, interaction: discord.Interaction, button: discord.ui.Button):
      await self.button("rock", interaction, button)

  @discord.ui.button(label='Paper', style=discord.ButtonStyle.blurple, emoji='📄')
  async def paperButton(self, interaction: discord.Interaction, button: discord.ui.Button):
      await self.button("paper", interaction, button)

  @discord.ui.button(label='Scissors', style=discord.ButtonStyle.blurple, emoji='✂️')
  async def scissorsButton(self, interaction: discord.Interaction, button: discord.ui.Button):
      await self.button("scissors", interaction, button)

  async def getHand(self):
    await self.wait()
    return self.chosenHand


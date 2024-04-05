import discord
from discord import app_commands
from discord.ext import commands
from GameBot.cogs.helpClasses.buttonsDuel import DuelView
from GameBot.cogs.helpClasses.buttonsHand import HandView
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.utils.interactionRespond import interactionRespond

#main class for rps game
class rockPaperScissors(commands.Cog):
  def __init__(self, bot):
        self.bot = bot
    
  @app_commands.command(name='rps', description='Play Rock Paper Scissors with someone!')
  async def rps(self, interaction: discord.Interaction, challengeduser: discord.Member):
    
    self.challengedUser = challengeduser
    self.challengingUser = interaction.user

    if self.challengedUser.id ==  self.challengingUser.id:
      await interaction.response.send_message("You cannot challenge yourself!")
      return
  
    embed = Embed()
    view = DuelView(interaction.user,challengeduser,self.bot)
    duelInstance = HandView(interaction.user,challengeduser,self.bot)

    await interaction.response.send_message(embed=embed.challengeDuel( self.challengingUser,self.challengedUser),view=view)
    await view.wait()
    if(view.buttonPressed):
      await interaction.edit_original_response(embed = embed.choseHands(duelInstance.choices()),view = duelInstance)
      choices = await duelInstance.getHands()
      if self.checkIfPicked(choices):
        outcome = self.deciceDuel(choices)
        await interaction.edit_original_response(embed=embed.returnDuel(self.challengingUser,self.challengedUser, outcome),view=None)
      else:
        await interaction.edit_original_response(embed=embed.duelTerminated(),view=None)
    else:
      await interaction.edit_original_response(embed=embed.duelDeclined(self.challengedUser),view=None)
    await interactionRespond(interaction)


  def deciceDuel(self,choice: dict):
    beats = {
      '🗿': '✂️',
      '✂️': '📄',
      '📄': '🗿',
    }
    hand = list(choice.values())
    if hand[0].name == hand[1].name:
      outcome = "tie"
    elif hand[0].name == beats[hand[1].name]:
      outcome = "lose"
    else:
      outcome = "win"

    ret = {self.challengingUser: hand[0].name,self.challengedUser: hand[1].name}

    return [outcome,ret]

  def checkIfPicked(self,choice: dict):
    hand = list(choice.values())
    return all(i != None for i in hand)
        
async def setup(bot):
  await bot.add_cog(rockPaperScissors(bot))
  


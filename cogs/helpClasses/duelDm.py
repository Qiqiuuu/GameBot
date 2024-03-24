import discord
from discord.ext import commands

from cogs.helpClasses.buttonsDm import dmView


class duelDm():
  def __init__(self,challenger: discord.User,challenged: discord.User):
    self.challerger = challenger
    self.challerged = challenged
    self.chall = {challenged:challenger,
             challenger:challenged
            }

  
  async def sendDm(self,user):
    embed = discord.Embed(title="Choose your Hand:", description=f"Against: {self.chall[user]}", color=0x000000)
    view = dmView(user)
    await user.send(embed=embed, view=view)
    return await view.getHand()


  async def duelDecider(self):
    challengedChoice = await self.sendDm(self.challerged)
    challengerChoice = await self.sendDm(self.challerger)
    print(challengedChoice)
    print(challengerChoice)
    beats = {
      'rock': 'scissors',
      'scissors': 'paper',
      'paper': 'rock',
    }

    if challengerChoice == challengedChoice:
      outcome = "tie"
    elif challengerChoice == 'beats[challengedChoice]':
      outcome = "loses"
    else:
      outcome = "wins"

    return outcome
    
    
import discord
from cogs.helpClasses.buttonsDm import DmView
import asyncio


class DuelDm():
  def __init__(self,challengingUser, challengedUser, bot):
    self.bot = bot
    self.challengingUser = challengingUser
    self.challengedUser = challengedUser
    self.chall = {
      challengedUser: challengingUser, 
      challengingUser: challengedUser
    }

  
  async def sendDm(self,user):
    embed = discord.Embed(title="Choose your Hand:", description=f"Against: {self.chall[user]}", color=0x000000)
    view = DmView(user,self.bot)
    await user.send(embed=embed, view=view)
    return await view.getHand()


  async def duelDecider(self):
    challengedChoice_coroutine = self.sendDm(self.challengedUser)
    challengingChoice_coroutine = self.sendDm(self.challengingUser)
    challengedChoice, challengingChoice =  await asyncio.gather(challengedChoice_coroutine, challengingChoice_coroutine)
    beats = {
      'rock': 'scissors',
      'scissors': 'paper',
      'paper': 'rock',
    }

    if challengingChoice == challengedChoice:
      outcome = "tie"
    elif challengedChoice in beats and challengingChoice == beats[challengedChoice]:
      outcome = "lose"
    else:
      outcome = "win"

    return [outcome,challengingChoice,challengedChoice]

    
    
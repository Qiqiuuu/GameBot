import discord
from discord import client
from discord.ext import commands
import asyncio
from cogs.helpClasses.buttonsDm import dmView


class duelDm():
  def __init__(self,challenger: discord.User,challenged: discord.User,bot):
    self.bot = bot
    self.challerger = challenger
    self.challerged = challenged
    self.chall = {challenged:challenger,
             challenger:challenged
            }

  
  async def sendDm(self,user):
    embed = discord.Embed(title="Choose your Hand:", description=f"Against: {self.chall[user]}", color=0x000000)
    view = dmView(user,self.bot)
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
    elif challengedChoice in beats and challengerChoice == beats[challengedChoice]:
      outcome = "loses"
    else:
      outcome = "wins"

    return outcome

    
    
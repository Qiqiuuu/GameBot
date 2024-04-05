from typing import Dict, List
import discord
from GameBot.utils.writeDictionary import writeDictionary
from GameBot.utils.writePlayersInLobby import writePlayersInLobby

#class for embeded messages
class Embed:
  def startLobby(self,gameName: str,players: List):
     embed = discord.Embed(title=f"Creating lobby for {gameName}", description = f"Current players in lobby:\n {writePlayersInLobby(players)}",color=0x000000)
     return embed


  def closingLobby(self,gameName: str,players: List):
    embed = discord.Embed(
      title=f"Lobby was created for {gameName}",
      description = f"Current players in lobby:\n {writePlayersInLobby(players)}The game is starting...",
      color=0x000000)
    return embed

  def choseHands(self,playersChoices: Dict):
    embed = discord.Embed(
      title="Chose your Hand", 
      description = f"{writeDictionary(playersChoices)}",
      color=0x000000)
    return embed

  def duelDeclined(self,challengedUser):
    embed = discord.Embed(
      title="Duel Declined",
      description = f"{challengedUser.mention} chickened out!",
      color=0x000000
    )
    return embed

  def duelTerminated(self):
    embed = discord.Embed(
      title="Duel Terminated",
      description = "Duel was terminated due to a lack of response",
      color=0x000000
    )
    return embed
                      
  #creates embed for challenge
  def challengeDuel(self,challengingUser,challengedUser):
    embed = discord.Embed(
      title="Upcoming Duel ", 
      description=f"{challengingUser.mention} challenged {challengedUser.mention} in Rock, Paper, Scissors",
      color=0x000000)
    embed.set_thumbnail(url = challengedUser.display_avatar.url)
    return embed

  #creates embed for duel outcome
  def returnDuel(self,challengingUser,challengedUser,outcome):
    messageDecider = {
      "tie": f"The duel has ended as a tie between {challengingUser.mention} and {challengedUser.mention}",
      "win": f"{challengingUser.mention} has won the duel against {challengedUser.mention}",
      "lose": f"{challengedUser.mention} has won the duel against {challengingUser.mention}"
    }
    embed = discord.Embed(
      title="Duel Ended", 
      description=f"{messageDecider[outcome[0]]}\n{writeDictionary(outcome[1])}",
      color=0x000000)
    return embed


  
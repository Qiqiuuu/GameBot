import discord
from discord.ext import tasks
from dotenv import main
from cogs.helpClasses.embed import Embed


class Lobby(discord.ui.View):
  def __init__(self,bot,gameName: str,):
    self.bot = bot
    self.gameName = gameName
    self.playersList = []

def getEmbed(self):
  embed = Embed()
  return embed.startLobby(self.gameName, self.playersList)


async def creatingLobby(self, interaction: discord.Interaction):
  self.embedMessage = await interaction.response.send_message(embed=self.getEmbed(), view=self)
  self.updateEmbed.start()

@discord.ui.button(label='Add to Lobby', style=discord.ButtonStyle.green)
async def handleButton(self, interaction: discord.Interaction, button: discord.ui.Button):
  if interaction.user.id not in self.playersList:
      self.addPlayer(interaction.user.id)
      await self.embedMessage.edit_original_response(embed=self.getEmbed())

def addPlayer(self, player):
  self.playersList.append(player)

def returnList(self):
  return self.playersList


@tasks.loop(seconds=30)
async def updateEmbed(self):
  await self.embedMessage.edit(embed=self.getEmbed())

def stop(self):
  self.updateEmbed.stop()





  
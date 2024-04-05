import discord
from discord.ext import commands

#bot class
class gameBot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix='!', intents = discord.Intents.all())
  
  async def on_ready(self):
    print(f'{self} has connected to Discord!')
    await self.load_extension('cogs.rockPaperScissors')
    await self.load_extension('cogs.russianRoulette')
    synced = await self.tree.sync()
    print(f'Synced {len(synced)} commands.')

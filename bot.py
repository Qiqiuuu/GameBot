import discord
from discord.ext import commands

class gameBot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix='!', intents = discord.Intents.all(), application_id = '1221075051202482207')
  
  async def on_ready(self):
    print(f'{self} has connected to Discord!')
    await self.load_extension('cogs.rockPaperScissors')
    synced = await self.tree.sync()
    print(f'Synced {len(synced)} commands.')
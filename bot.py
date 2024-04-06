import discord
from discord.ext import commands
from GameBot.cogs.dataBase import DataBase


# bot class
class gameBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        self.dataBase = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.load_extension('cogs.rockPaperScissors')
        await self.load_extension('cogs.russianRoulette')
        synced = await self.tree.sync()
        self.dataBase = DataBase()

        print(f'Synced {len(synced)} commands.')

    def getdataBase(self):
        return self.dataBase

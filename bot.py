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
        print(f'Synced {len(synced)} commands.')
        self.dataBase = DataBase()
        self.fetchDataToDataBase()
        print(f"Fetched data")

    def getdataBase(self):
        return self.dataBase

    def fetchDataToDataBase(self):
        print(f"Fetching Guilds")
        for guild in self.guilds:
            self.dataBase.checkGuild(guild)
            print(f"Fetching members from guild: {guild.name}")
            for member in guild.members:
                if not member.bot:
                    self.dataBase.checkMember(member)
            print(f"Fetched members from guild: {guild.name}")

import discord
from discord.ext import commands
from cogs.dataBase import DataBase
from cogs.casino import Casino


# bot class
class GameBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        self.dataBase = None
        self.casinoDataBase = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.dataBase = DataBase(self)
        await self.load_extension('cogs.rockPaperScissors')
        await self.load_extension('cogs.russianRoulette')
        await self.load_extension('cogs.dataBase')
        await self.load_extension('cogs.casino')
        await self.load_extension('cogs.serviceProfiles')
        self.casinoDataBase = Casino(self)
        self.checkGuilds()
        await self.casinoDataBase.afterInit()
        synced = await self.tree.sync()
        print(f'Synced {len(synced)} commands.')
        self.fetchDataToDataBase()
        self.fetchGamesToUsers(synced)
        print(f"Fetched data")
        print(f"Bot ready!")

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

    def fetchGamesToUsers(self, synced):
        print("Fetching Games")
        for command in synced:
            if command.name not in {'profile', 'shop', "setcasinochannel", "checkprofile", "setserviceprofile"}:
                for guild in self.guilds:
                    self.dataBase.addGame(guild, command.id, command.name)

    def checkGuilds(self):
        print("Getting casino channels")
        for guild in self.guilds:
            self.casinoDataBase.checkGuild(guild)

import time

import discord
from discord import app_commands
from discord.ext import commands
from GameBot.cogs.helpClasses.lobby import Lobby


class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.playerList = None
        self.interaction = None
        self.bot = bot

    @app_commands.command(name='russianroulette', description='Let roulette spin!')
    async def russianRoulette(self, interaction: discord.Interaction):
        lobby = Lobby(self.bot,"Russian Roulette")
        await lobby.creatingLobby(interaction)
        self.playerList,self.interaction, = await lobby.returnList()
        time.sleep(2)



async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))

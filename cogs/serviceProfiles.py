import random
import asyncio

import discord
from discord import app_commands, Embed
from discord.ext import commands


class serviceProfiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.dataBase = self.bot.getdataBase()

    @app_commands.command(name='checkprofile', description='Check your Profile!')
    async def checkProfile(self, interaction: discord.Interaction, user: discord.Member, service: str):
        return

    @app_commands.command(name='setserviceprofile', description='Add your Service Profile!')
    async def addServiceProfile(self, interaction: discord.Interaction, user: discord.Member, service: str, id: str):
        self.dataBase.setServiceProfile(user, service, id)


async def setup(bot):
    await bot.add_cog(serviceProfiles(bot))

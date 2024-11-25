import random
import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.embed import Embed
class serviceProfiles(commands.cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
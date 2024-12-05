import json
import os
import random
import asyncio

import discord
import requests
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.embed import Embed
from dotenv import load_dotenv

from GameBot.utils.interactionRespond import interactionRespond


class serviceProfiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.dataBase = self.bot.getdataBase()
        load_dotenv()
        self.STEAM_KEY = os.getenv('STEAM_API')

    @app_commands.command(name='checkprofile', description='Check your Profile!')
    async def checkProfile(self, interaction: discord.Interaction, user: discord.Member, service: str):
        if self.dataBase.getServiceProfile(user, service) is not None:
            match service:
                case "steam":
                    await interaction.response.send_message(embed=self.embed.create_steam_profile_embed(
                        self.steamAPI(self.dataBase.getServiceProfile(user, service))))
        else:
            await interaction.response.send_message("Something went wrong!")
        await interactionRespond(interaction)

    @app_commands.command(name='setserviceprofile', description='Add your Service Profile!')
    async def setServiceProfile(self, interaction: discord.Interaction, user: discord.Member, service: str, id: str):
        if service in ["steam", "battle.net"]:
            self.dataBase.addServiceProfile(user.guild, user, service, id)
            await interaction.response.send_message("You've set your Profile")
        else:
            await interaction.response.send_message("Wrong service!")
        await interactionRespond(interaction)

    def steamAPI(self, id: str):
        response = requests.get(
            "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json".format(
                self.STEAM_KEY, id)).text
        res = json.loads(response)

        games = requests.get(
            'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&include_appinfo=True&include_played_free_games=True&format=json'.format(
                self.STEAM_KEY, id)).text
        game = json.loads(games)

        hours = 0
        for i in game["response"]["games"]:
            hours = hours + i["playtime_forever"]

        lvl = requests.get(
            "http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={}&steamid={}&format=json".format(
                self.STEAM_KEY, id)).text
        lvl = json.loads(lvl)

        status = res["response"]["players"][0]["profilestate"]
        stat = {0: "Offline", 1: "Online", 2: "Busy", 3: "Away", 4: "Snooze"}
        status = stat[status]

        ret = {"steam_id": res["response"]["players"][0]["steamid"],
               "avatar": res["response"]["players"][0]["avatarmedium"],
               "nick": res["response"]["players"][0]["personaname"],
               "games": game["response"]["game_count"],
               "hours": int(hours / 60),
               "lvl": lvl["response"]["player_level"],
               "time": res["response"]["players"][0]["timecreated"],
               "status": status,
               "url": res["response"]["players"][0]["profileurl"]
               }
        return ret


async def setup(bot):
    await bot.add_cog(serviceProfiles(bot))

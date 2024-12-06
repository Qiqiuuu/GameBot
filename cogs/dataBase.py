import datetime
from discord import app_commands
from discord.ext import commands
from pymongo import MongoClient
import discord
from dotenv import load_dotenv
import os
import urllib.parse
from ..cogs.helpClasses.embed import Embed


class DataBase(commands.Cog):



    #CAŁA BAZA DO PRZEROBIENIA ZAMIAST SERVERO CENTRALNA TO UZYTKOWNIKOCENTALNA Z SERVERAMI W SRODKU I ICH UNIKALNYMI STATAMI



    def __init__(self, bot):
        self.bot = bot
        self.client = None
        load_dotenv()
        self.myPassword = os.getenv('PASSWD')
        self.myLogin = os.getenv('LOGIN')
        self.loginToMongo()
        self.db = self.client['GameBot']
        self.guilds = self.db['guilds']

    def loginToMongo(self):
        escaped_username = urllib.parse.quote_plus(self.myLogin)
        escaped_password = urllib.parse.quote_plus(self.myPassword)
        self.client = MongoClient(
            f"mongodb+srv://{escaped_username}:{escaped_password}@gamebot.5w0xcvj.mongodb.net/?retryWrites=true&w=majority&appName=GameBot")
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    @app_commands.command(name='profile', description="Check member's profile")
    async def profile(self, interaction: discord.Interaction, membertocheck: discord.Member):
        memberData = self.getMember(membertocheck)
        embed = Embed()
        await interaction.response.send_message(embed=embed.profile(memberData, interaction.guild))

    def checkGuild(self, guild: discord.Guild):
        if not self.guilds.find_one({"_id": guild.id}):
            self.guilds.insert_one({
                "_id": guild.id,
                "name": guild.name,
                "members": {}
            })
            print(f"Created new guild: {guild.name} - {datetime.datetime.now()}")

    def checkMember(self, member: discord.Member):
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if not guildData:
            self.checkGuild(member.guild)
        if str(member.id) not in guildData['members']:
            self.guilds.update_one(
                {"_id": member.guild.id},
                {"$set": {
                    "members." + str(member.id): {
                        "id": member.id,
                        "name": member.name,
                        "coins": 200,
                        "timeSpentOnVC": 0,
                        "games": {},
                        "serviceProfiles": {}
                    }
                }}
            )
            print(f"Added new member: {member.name} to guild: {member.guild.name} - {datetime.datetime.now()}")

    def addMoney(self, member: discord.Member, amount: int):
        self.checkMember(member)
        self.guilds.update_one(
            {"_id": member.guild.id, f"members.{str(member.id)}": {"$exists": True}},
            {"$inc": {f"members.{str(member.id)}.coins": amount}}
        )
        print(
            f"Added coins to member: {member.name} in guild: {member.guild.name}, amount: {amount} - {datetime.datetime.now()}")

    def takeMoney(self, member: discord.Member, amount: int):
        self.checkMember(member)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if guildData['members'][str(member.id)]['coins'] >= amount:
            self.guilds.update_one(
                {"_id": member.guild.id},
                {"$inc": {f"members.{str(member.id)}.coins": -amount}}
            )
            print(
                f"Took coins from member: {member.name} in guild: {member.guild.name}, amount: -{amount} - {datetime.datetime.now()}")
            return True
        else:
            return False

    def addTime(self, member: discord.Member, amount: int):
        self.checkMember(member)
        self.guilds.update_one(
            {"_id": member.guild.id, f"members.{str(member.id)}": {"$exists": True}},
            {"$inc": {f"members.{str(member.id)}.timeSpentOnVC": amount}}
        )
        print(
            f"Added time to member: {member.name} in guild: {member.guild.name}, amount: {amount} - {datetime.datetime.now()}")

    def getMember(self, member: discord.Member):
        self.checkMember(member)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        return guildData['members'][str(member.id)]

    def addGame(self, guild: discord.Guild, gameID, gameName):
        self.checkGuild(guild)
        guildData = self.guilds.find_one({"_id": guild.id})
        for member in guild.members:
            if not member.bot:
                if str(gameID) not in guildData['members'][str(member.id)]['games']:
                    self.guilds.update_one(
                        {"_id": member.guild.id, f"members.{str(member.id)}": {"$exists": True}},
                        {"$set": {f"members.{str(member.id)}.games.{str(gameID)}": {
                            "gameID": gameID,
                            "gameName": gameName,
                            "W": 0,
                            "L": 0,
                            "Profit": 0
                        }}}
                    )
                    print(f"Added new game {gameName} to guild {guild.name}")

    def addServiceProfile(self, guild: discord.Guild, user: discord.Member, serviceName, profileID):
        self.checkGuild(guild)
        for member in guild.members:
            if not member.bot and member == user:
                self.guilds.update_one(
                    {"_id": member.guild.id, f"members.{str(member.id)}": {"$exists": True}},
                    {"$set": {f"members.{member.id}.serviceProfiles.{serviceName}": profileID}},
                    upsert=True
                )
                print(f"Added new Service {serviceName} to member {member.id}")

    def getServiceProfile(self, member: discord.Member, serviceName):
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if guildData is None:
            return None
        members = guildData.get('members', {})
        memberData = members.get(str(member.id))
        serviceProfile = memberData.get("serviceProfiles")
        if memberData is None:
            return None
        return serviceProfile.get(serviceName, None)

    def addLose(self, member: discord.Member, gameID, amount: int):
        self.takeMoney(member, amount)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        memberData = guildData['members'][str(member.id)]

        if str(gameID) in memberData["games"]:
            self.guilds.update_one(
                {"_id": member.guild.id, f"members.{str(member.id)}.games.{str(gameID)}": {"$exists": True}},
                {"$inc": {f"members.{str(member.id)}.games.{str(gameID)}.L": 1}}
            )
            self.guilds.update_one(
                {"_id": member.guild.id, f"members.{str(member.id)}.games.{str(gameID)}": {"$exists": True}},
                {"$inc": {f"members.{str(member.id)}.games.{str(gameID)}.Profit": -amount}}
            )
            print(
                f"Updated game stats for member: {member.name} in guild: {member.guild.name}, gameID: {gameID}, amount: {-amount} - {datetime.datetime.now()}")

    def addWin(self, member: discord.Member, gameID, amount: int):
        self.addMoney(member, amount)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        memberData = guildData['members'][str(member.id)]

        if str(gameID) in memberData["games"]:
            self.guilds.update_one(
                {"_id": member.guild.id, f"members.{str(member.id)}.games.{str(gameID)}": {"$exists": True}},
                {"$inc": {f"members.{str(member.id)}.games.{str(gameID)}.W": 1}}
            )
            self.guilds.update_one(
                {"_id": member.guild.id, f"members.{str(member.id)}.games.{str(gameID)}": {"$exists": True}},
                {"$inc": {f"members.{str(member.id)}.games.{str(gameID)}.Profit": amount}}
            )
            print(
                f"Updated game stats for member: {member.name} in guild: {member.guild.name}, gameID: {gameID}, amount: {amount} - {datetime.datetime.now()}")

    def getCoins(self, member: discord.Member):
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if str(member.id) in guildData['members']:
            return guildData['members'][str(member.id)]['coins']

    def getProfileID(self, member: discord.Member):
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if str(member.id) in guildData['members']:
            return guildData['members'][str(member.id)]['profiles']


async def setup(bot):
    await bot.add_cog(DataBase(bot))

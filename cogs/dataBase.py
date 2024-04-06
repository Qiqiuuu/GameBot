import datetime

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import discord
from dotenv import load_dotenv
import os
import urllib.parse


class DataBase:
    def __init__(self):
        self.client = None
        load_dotenv()
        self.myPassword = os.getenv('PASSWD')
        self.loginToMongo()
        self.db = self.client['GameBot']  # Use your database name here
        self.guilds = self.db['guilds']  # Use your collection name here

    def loginToMongo(self):
        escaped_username = urllib.parse.quote_plus('Qiqiu')
        escaped_password = urllib.parse.quote_plus(self.myPassword)
        # Connect to MongoDB
        self.client = MongoClient(
            f"mongodb+srv://{escaped_username}:{escaped_password}@gamebot.5w0xcvj.mongodb.net/?retryWrites=true&w=majority&appName=GameBot")
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

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
                        "money": 200,
                        "timeSpentOnVC": 0
                    }
                }}
            )
            print(f"Added new member: {member.name} to guild: {member.guild.name} - {datetime.datetime.now()}")

    def addMoney(self, member: discord.Member, amount: int):
        self.checkMember(member)
        self.guilds.update_one(
            {"_id": member.guild.id, "members." + str(member.id): {"$exists": True}},
            {"$inc": {"members." + str(member.id) + ".money": amount}}
        )
        print(f"Added money to member: {member.name} in guild: {member.guild.name}, amount: {amount} - {datetime.datetime.now()}")

    def takeMoney(self, member: discord.Member, amount: int):
        self.checkMember(member)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        if guildData['members'][str(member.name)]['money'] >= amount:
            self.guilds.update_one(
                {"_id": member.guild.id},
                {"$inc": {"members." + str(member.id) + ".money": -amount}}
            )
            print(f"Took money from member: {member.name} in guild: {member.guild.name}, amount: {amount} - {datetime.datetime.now()}")
            return True
        else:
            return False

    def addTime(self, member: discord.Member, amount: int):
        self.checkMember(member)
        self.guilds.update_one(
            {"_id": member.guild.id, "members." + str(member.id): {"$exists": True}},
            {"$inc": {"members." + str(member.id) + ".timeSpentOnVC": amount}}
        )
        print(f"Added time to member: {member.name} in guild: {member.guild.name}, amount: {amount} - {datetime.datetime.now()}")

    def getMember(self, member: discord.Member):
        self.checkMember(member)
        guildData = self.guilds.find_one({"_id": member.guild.id})
        return guildData['members'][str(member.id)]




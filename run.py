import discord
import os
from dotenv import load_dotenv
from bot import gameBot
from utils.keepAlive import keepAlive


#bot runner

load_dotenv()
myToken = os.getenv('TOKEN')

bot = gameBot()

keepAlive()

bot.run(str(myToken))
  

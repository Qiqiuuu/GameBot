import os
from dotenv import load_dotenv
from bot import gameBot


#bot runner

load_dotenv()
myToken = os.getenv('TOKEN')

bot = gameBot()

bot.run(str(myToken))
  

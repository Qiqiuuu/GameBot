import datetime
import os
from dotenv import load_dotenv
from bot import GameBot

# bot runner

load_dotenv()
myToken = os.getenv('TOKEN')

bot = GameBot()

joinTimes = {}


@bot.event
async def on_voice_state_update(member, before, after):
    dataBase = bot.getdataBase()

    if before.channel is None and after.channel is not None:
        joinTimes[member.id] = datetime.datetime.now()
        print(f"Member {member.name} joined to voice channel in {member.guild.name} - {datetime.datetime.now()}")
    elif before.channel is not None and after.channel is None:
        if member.id in joinTimes:
            delta = datetime.datetime.now() - joinTimes[member.id]
            minutesSpentOnVC = int(delta.total_seconds() / 60)
            dataBase.addMoney(member, int(minutesSpentOnVC/10))
            dataBase.addTime(member, minutesSpentOnVC)
            del joinTimes[member.id]


bot.run(str(myToken))


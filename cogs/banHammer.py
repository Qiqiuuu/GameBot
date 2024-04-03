from discord.ext import commands
import asyncio

#unused class for bans/kicks etc
class BanHammer(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  async def ban(self, guild ,toBan, minutes: int):

      await toBan.ban(reason="Banned for a specific number of minutes")
      delay = minutes * 60
      await asyncio.sleep(delay)
      await guild.unban(toBan)

async def setup(bot):
  await bot.add_cog(BanHammer(bot))
  
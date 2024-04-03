import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.buttonsDuel import DuelView
from cogs.helpClasses.duelDm import DuelDm
from cogs.helpClasses.embed import Embed

#main class for rps game
class rockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='rps', description='Play Rock Paper Scissors with me!')
    async def rps(self, interaction: discord.Interaction, challengeduser: discord.Member):

      if challengeduser.id == interaction.user.id:
        await interaction.response.send_message("You cannot challenge yourself!")
        return
  
      embed = Embed()
      view = DuelView(interaction.user,challengeduser,self.bot)
      duelInstance = DuelDm(interaction.user,challengeduser,self.bot)

      await interaction.response.send_message(embed=embed.challengeDuel(interaction.user,challengeduser),view=view)

      await view.wait()
      if(view.buttonPressed):
        outcome = await duelInstance.duelDecider()
        await interaction.followup.send(embed=embed.returnDuel(interaction.user,challengeduser, outcome))
      else:
        await interaction.followup.send(f"{challengeduser.mention} declined the duel")
        await interaction.response.defer()
        
async def setup(bot):
  await bot.add_cog(rockPaperScissors(bot))
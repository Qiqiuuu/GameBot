import discord
from discord import app_commands
from discord.ext import commands




class rockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='rps', description='Play Rock Paper Scissors with me!')
    async def rps(self, interaction: discord.Interaction, challengeduser: discord.User, stake: int):
      
      embed = discord.Embed(title="Upcoming Duel ", description=f"{interaction.user.mention} challenged {challengeduser.mention} in Rock, Paper, Scissors\n Stake: {stake} min ban", color=0x000000)

      embed.set_thumbnail(url = challengeduser.display_avatar.url)
      
      button = discord.Button(
          label='Accept Duel',
          style=discord.ButtonStyle.green
      )
      action_row = discord.ActionRow(button)

      
      
      await interaction.response.send_message(embed=embed,components=[action_row])



async def setup(bot):
  await bot.add_cog(rockPaperScissors(bot))
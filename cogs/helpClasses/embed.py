import discord

class Embed:
  def __init__(self,challengedUser,challengingUser):
    self.challengedUser = challengedUser
    self.challengingUser = challengingUser


  def challengeDuel(self):
    embed = discord.Embed(title="Upcoming Duel ", description=f"{self.challengingUser.mention} challenged {self.challengedUser.mention} in Rock, Paper, Scissorsban", color=0x000000)
    embed.set_thumbnail(url = self.challengedUser.display_avatar.url)
    return embed

  def returnDuel(self,outcome):
    messageDecider = {
      "tie": f"Duel has ended as a tie betweeen {self.challengingUser.mention} and {self.challengedUser.mention}",
      "win": f"{self.challengingUser.mention} has won the duel against {self.challengedUser.mention}",
      "lose": f"{self.challengedUser.mention} has won the duel against {self.challengingUser.mention}"
    }
    embed = discord.Embed(title="Duel Ended", description= 
                          f"{messageDecider[outcome[0]]}\n{self.challengingUser.mention} chose {outcome[1]}\n{self.challengedUser.mention} chose {outcome[2]}"
                          ,color=0x000000)
    return embed

  def loser(self,outcome):
    loser = {
      "tie": None,
      "win":self.challengedUser,
      "lose":self.challengingUser
    }
    return loser[outcome[0]]
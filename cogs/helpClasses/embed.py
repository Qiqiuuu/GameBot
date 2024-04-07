from typing import Dict, List
import discord
from utils.writePlayersInLobby import writePlayersInLobby


# class for embeded messages
class Embed:
    def embedTemplate(self, title: str, description: str, color: int = 0x000000, thumbnail_url: str = None,
                      footer: str = None):
        embed = discord.Embed(title=title, description=description, color=color)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        return embed

    def isFree(self, bet: int):
        return f'{bet} :coin:' if bet > 0 else 'Free'

    def rouletteStart(self, players: dict):
        description = f"Are you ready to welcome Death? 💀\n{writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"Russian Roulette", description=description)

    def rouletteDied(self, deadPlayer: discord.Member, players: dict):
        description = f"{deadPlayer.mention} died! ☠️\n {writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"Russian Roulette", description=description)

    def rouletteSurvived(self, players: dict):
        description = f"No one died this time! 🍻\n{writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"Russian Roulette", description=description)

    def rouletteEnd(self, winner: discord.Member, wholeBet: int):
        description = f"{winner.mention} won{' '+str(wholeBet)+' :coin:' if wholeBet > 0 else ''}! 👏"
        return self.embedTemplate(title=f"Russian Roulette", description=description)

    def startLobby(self, gameName: str, players: list, bet: int):
        description = ""
        description += f"Lobby's entry fee: {self.isFree(bet)} \n"
        description += f"Current players in lobby: \n{writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"Creating lobby for {gameName}", description=description)

    def closingLobby(self, gameName: str, players: list):
        description = f"Current players in lobby: \n{writePlayersInLobby(players)}The game is starting ..."
        return self.embedTemplate(title=f"Lobby was created for {gameName}", description=description)

    def cancelLobby(self, gameName: str):
        description = f"Lobby for {gameName} was canceled!"
        return self.embedTemplate(title="Lobby Canceled!", description=description)

    def choseHands(self, playersChoices: dict):
        description = f"{writePlayersInLobby(playersChoices)}"
        return self.embedTemplate(title="Chose your Hand", description=description)

    def duelDeclined(self, challengedUser):
        description = f"{challengedUser.mention} chickened out!"
        return self.embedTemplate(title="Duel Declined", description=description)

    def duelTerminated(self):
        description = "Duel was terminated due to a lack of response"
        return self.embedTemplate(title="Duel Terminated", description=description)

    def challengeDuel(self, challengingUser, challengedUser):
        description = f"{challengingUser.mention} challenged {challengedUser.mention} in Rock, Paper, Scissors"
        return self.embedTemplate(title="Upcoming Duel", description=description,
                                  thumbnail_url=challengedUser.display_avatar.url)

    def returnDuel(self, outcome, choices):
        description = f"{outcome[1].mention} tied with {outcome[2].mention}!" if outcome[
            0] else f"{outcome[1].mention} defeated {outcome[2].mention}!"
        description += f"\n{writePlayersInLobby(choices)}"
        return self.embedTemplate(title="Duel Ended", description=description)

    def profile(self, memberData: dict, guild: discord.Guild):
        member = guild.get_member(memberData['id'])
        description = f":coin: Coins: {memberData['coins']}\n:timer: Voice Channels Time: {memberData['timeSpentOnVC']} min\n"
        for game in memberData['games']:
            stats = memberData['games'][game]
            description += f"{stats['gameName']}:\n 　　W: {stats['W']} 　L: {stats['L']} 　Game Profit: {stats['Profit']}\n"

        return self.embedTemplate(title=f"{member.display_name}'s profile",
                                  description=description,
                                  thumbnail_url=member.display_avatar.url)

from datetime import datetime
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
        return self.embedTemplate(title=f"**Russian Roulette**", description=description)

    def rouletteDied(self, deadPlayer: discord.Member, players: dict, round: int):
        description = f"**Round {round}**\n"
        description += f"{deadPlayer.mention} **died!** ☠️\n {writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"**Russian Roulette**", description=description)

    def rouletteSurvived(self, players: dict, round: int):
        description = f"**Round {round}**\n"
        description += f"No one died this time! 🍻\n{writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"**Russian Roulette**", description=description)

    def rouletteEnd(self, winner: discord.Member, wholeBet: int):
        description = f"{winner.mention} **won{' ' + str(wholeBet) + ' :coin:' if wholeBet > 0 else ''}!** 👏"
        return self.embedTemplate(title=f"**Russian Roulette**", description=description)

    def startLobby(self, gameName: str, players: list, bet: int):
        description = ""
        description += f"**Lobby's entry fee:** {self.isFree(bet)} \n"
        description += f"Current players in lobby: \n{writePlayersInLobby(players)}"
        return self.embedTemplate(title=f"**Creating lobby for {gameName}**", description=description)

    def closingLobby(self, gameName: str, players: list):
        description = f"Current players in lobby: \n{writePlayersInLobby(players)}The game is starting ..."
        return self.embedTemplate(title=f"**Lobby was created for {gameName}**", description=description)

    def cancelLobby(self, gameName: str):
        description = f"Lobby for {gameName} was canceled!"
        return self.embedTemplate(title="**Lobby Canceled!**", description=description)

    def choseHands(self, playersChoices: dict):
        description = f"{writePlayersInLobby(playersChoices)}"
        return self.embedTemplate(title="**Chose your Hand:**", description=description)

    def duelDeclined(self, challengedUser):
        description = f"{challengedUser.mention} chickened out!"
        return self.embedTemplate(title="**Duel Declined**", description=description)

    def duelTerminated(self):
        description = "Duel was terminated due to a lack of response"
        return self.embedTemplate(title="**Duel Terminated**", description=description)

    def challengeDuel(self, challengingUser, challengedUser, bet):
        description = f"{challengingUser.mention} challenged {challengedUser.mention} in:\n**Rock, Paper, Scissors!**"
        description += f"\n**Bet:** {bet} :coin:" if bet > 0 else ""
        return self.embedTemplate(title="**Upcoming Duel!**", description=description,
                                  thumbnail_url=challengedUser.display_avatar.url)

    def returnDuel(self, outcome, choices, bet):
        description = f"{outcome[1].mention} tied with {outcome[2].mention}!" if outcome[
            0] else f"{outcome[1].mention} defeated {outcome[2].mention}!"
        description += "\n{outcome[1].mention} won {bet} :coin:" if bet > 0 and not outcome[0] else ""
        description += f"\n{writePlayersInLobby(choices)}"
        return self.embedTemplate(title="**Duel Ended**", description=description)

    def profile(self, memberData: dict, guild: discord.Guild):
        gamesEmoji = {'rps': ':rock:', 'russianroulette': ':gun:'}
        gamesNames = {'rps': 'Rock, Paper, Scissors', 'russianroulette': 'Russian Roulette'}
        member = guild.get_member(memberData['id'])
        description = f":coin: **Coins:** {memberData['coins']}\n:timer: **Voice Channels Time:** {int(memberData['timeSpentOnVC'] / 60)}h\n"
        for game in memberData['games']:
            stats = memberData['games'][game]
            description += f"{gamesEmoji[stats['gameName']]} **{gamesNames[stats['gameName']]}:**\n 　　W: {stats['W']} 　L: {stats['L']} 　Game Profit: {stats['Profit']}\n"

        return self.embedTemplate(title=f"**{member.display_name}'s profile**",
                                  description=description,
                                  thumbnail_url=member.display_avatar.url)

    def casinoWelcome(self):
        description = f"Choose from the list, game which you would like to play and join it, then leave it!"
        return self.embedTemplate(title="Welcome to the Casino!", description=description)

    def casinoLobby(self, playerList: dict):
        description = f"Current playing users: \n"
        for game, players in playerList.items():
            playersStr = ', '.join(player.global_name for player in players)
            description += f"**{game}:** {playersStr}\n"
        return self.embedTemplate(title="Casino Lobby", description=description)

    def blackjackHelp(self):
        description = f"tu kiedyś będzie help"
        return self.embedTemplate(title="Black Jack Help", description=description)

    def mainBlackJack(self, cardsOnTable: dict):
        description = f"Croupier Cards: {' '.join(cardsOnTable['croupier'])}\n"
        for player, cards in cardsOnTable.items():
            if player != 'croupier':
                description += f"{player}: {' '.join(cards)}"
        return self.embedTemplate(title="Black Jack", description=description)

    def waitingBlackJack(self):
        description = f"Join Black Jack lobby to start a game"
        return self.embedTemplate(title="Black Jack Waiting Room", description=description)

    def setService(self):
        description = f"You've set your Profile"
        return self.embedTemplate(title="Set your Profile", description=description)

    def create_steam_profile_embed(self, ret):
        creation_time = datetime.utcfromtimestamp(ret["time"]).strftime('%Y-%m-%d %H:%M:%S')

        # Create the embed
        embed = discord.Embed(
            title=f"{ret['nick']}'s Steam Profile",
            description=f"Click [here]({ret['url']}) to view the full profile.",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=ret['avatar'])

        embed.add_field(name="Steam ID", value=ret['steam_id'], inline=False)
        embed.add_field(name="Games Owned", value=str(ret['games']), inline=True)
        embed.add_field(name="Total Hours Played", value=f"{ret['hours']} hours", inline=True)
        embed.add_field(name="Steam Level", value=str(ret['lvl']), inline=True)
        embed.add_field(name="Account Created", value=creation_time, inline=True)
        embed.add_field(name="Status", value=ret['status'], inline=False)

        embed.set_footer(text=f"Profile of {ret['nick']}", icon_url=ret['avatar'])

        return embed

import discord
from discord import app_commands
from discord.ext import commands
from cogs.helpClasses.buttonsDuel import DuelView
from cogs.helpClasses.buttonsHand import HandView
from cogs.helpClasses.embed import Embed
from utils.interactionRespond import interactionRespond
from utils.interactionUserMember import interactionUserMember
from bot import GameBot


# main class for rps game
class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataBase = self.bot.getdataBase()
        self.gameID = 1221203592749514783

    @app_commands.command(name='rps', description='Play Rock Paper Scissors with someone!')
    async def rps(self, interaction: discord.Interaction, challengeduser: discord.Member, bet: int = 0):
        interactionUser = interactionUserMember(interaction)
        self.challengedUser = challengeduser
        self.challengingUser = interactionUser

        if self.challengedUser.id == self.challengingUser.id:
            await interaction.response.send_message("You cannot challenge yourself!")
            return

        if self.dataBase.getCoins(self.challengedUser) < bet:
            await interaction.response.send_message("Your opponent is too broke...")
            return

        embed = Embed()
        view = DuelView(interaction.user, challengeduser, self.bot)
        duelInstance = HandView(interaction.user, challengeduser, self.bot)

        await interaction.response.send_message(embed=embed.challengeDuel(self.challengingUser, self.challengedUser, bet)
                                                , view=view)

        await view.wait()
        if view.buttonPressed:
            await interaction.edit_original_response(embed=embed.choseHands(duelInstance.choices()), view=duelInstance)
            choices = await duelInstance.getHands()
            if self.checkIfPicked(choices):
                outcome = self.deciceDuel(choices)
                if not outcome[0]:
                    self.dataBase.addWin(outcome[1], self.gameID, bet)
                    self.dataBase.addLose(outcome[2], self.gameID, bet)
                await interaction.edit_original_response(
                    embed=embed.returnDuel(outcome, choices, bet), view=None)
            else:
                await interaction.edit_original_response(embed=embed.duelTerminated(), view=None)
        else:
            await interaction.edit_original_response(embed=embed.duelDeclined(self.challengedUser), view=None)
        await interactionRespond(interaction)

    def deciceDuel(self, choice: dict):
        beats = {
            '🗿': '✂️',
            '✂️': '📄',
            '📄': '🗿',
        }
        players = list(choice.keys())
        hand = list(choice.values())
        # [isTie,Winner,loser]
        if hand[0].name == hand[1].name:
            return [True, players[0], players[1]]
        elif hand[0].name == beats[hand[1].name]:
            return [False, players[1], players[0]]
        else:
            return [False, players[0], players[1]]

    def checkIfPicked(self, choice: dict):
        hand = list(choice.values())
        return all(i != None for i in hand)


async def setup(bot):
    await bot.add_cog(RockPaperScissors(bot))

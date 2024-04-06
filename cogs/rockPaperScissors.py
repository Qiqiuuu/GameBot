import discord
from discord import app_commands
from discord.ext import commands
from GameBot.cogs.helpClasses.buttonsDuel import DuelView
from GameBot.cogs.helpClasses.buttonsHand import HandView
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.utils.interactionRespond import interactionRespond
from GameBot.utils.interactionUserMember import interactionUserMember


# main class for rps game
class rockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='rps', description='Play Rock Paper Scissors with someone!')
    async def rps(self, interaction: discord.Interaction, challengeduser: discord.Member):
        interactionUser = interactionUserMember(interaction)
        self.challengedUser = challengeduser
        self.challengingUser = interactionUser

        if self.challengedUser.id == self.challengingUser.id:
            await interaction.response.send_message("You cannot challenge yourself!")
            return

        embed = Embed()
        view = DuelView(interaction.user, challengeduser, self.bot)
        duelInstance = HandView(interaction.user, challengeduser, self.bot)

        await interaction.response.send_message(embed=embed.challengeDuel(self.challengingUser, self.challengedUser),
                                                view=view)
        await view.wait()
        if view.buttonPressed:
            await interaction.edit_original_response(embed=embed.choseHands(duelInstance.choices()), view=duelInstance)
            choices = await duelInstance.getHands()
            if self.checkIfPicked(choices):
                outcome = self.deciceDuel(choices)
                await interaction.edit_original_response(
                    embed=embed.returnDuel(outcome,choices), view=None)
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
    await bot.add_cog(rockPaperScissors(bot))

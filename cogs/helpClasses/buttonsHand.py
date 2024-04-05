import discord
from typing import Optional
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.utils.interactionUserMember import interactionUserMember

class HandView(discord.ui.View):
    def __init__(self, challengingUser, challengedUser, bot):
        super().__init__()
        self.bot = bot
        self.chosenHands:dict[int, Optional[discord.PartialEmoji]] = {challengingUser.id: None, challengedUser.id: None,}
        self.playerChoices = {challengingUser: '❌', challengedUser: '❌'}

    async def button(self, hand: str, interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        embed = Embed()
        if interaction.user.id in self.chosenHands:
            await interaction.response.defer()
            self.chosenHands[interaction.user.id] = button.emoji
            self.playerChoices[interactionUser] = '✅'
            await interaction.edit_original_response(embed = embed.choseHands(self.choices()))
            if all(hand is not None for hand in self.chosenHands.values()):
                self.stop()
        else:
            await interaction.response.send_message(content=f"You are not participating in this duel!", ephemeral=True)
        await interaction.response.defer() if not interaction.response.is_done() else None

    @discord.ui.button(label='Rock', style=discord.ButtonStyle.blurple, emoji='🗿')
    async def rockButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button("rock", interaction, button)

    @discord.ui.button(label='Paper', style=discord.ButtonStyle.blurple, emoji='📄')
    async def paperButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button("paper", interaction, button)

    @discord.ui.button(label='Scissors', style=discord.ButtonStyle.blurple, emoji='✂️')
    async def scissorsButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button("scissors", interaction, button)

    async def getHands(self):
        await self.wait()
        return self.chosenHands
      
    def choices(self):
        return self.playerChoices
    


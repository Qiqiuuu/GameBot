import discord
from typing import Optional
from GameBot.cogs.helpClasses.embed import Embed
from GameBot.utils.interactionUserMember import interactionUserMember
from GameBot.utils.interactionRespond import interactionRespond

class HandView(discord.ui.View):
    def __init__(self, challengingUser: discord.Member, challengedUser: discord.Member, bot):
        super().__init__()
        self.bot = bot
        self.chosenHands:dict[discord.Member, Optional[discord.PartialEmoji]] = {challengingUser: None, challengedUser: None,}
        self.playerChoices = {challengingUser: '❌', challengedUser: '❌'}

    async def button(self,interaction: discord.Interaction, button: discord.ui.Button):
        interactionUser = interactionUserMember(interaction)
        embed = Embed()
        if interactionUser in self.chosenHands:
            await interaction.response.defer()
            self.chosenHands[interactionUser] = button.emoji
            self.playerChoices[interactionUser] = '✅'
            await interaction.edit_original_response(embed = embed.choseHands(self.choices()))
            if all(hand is not None for hand in self.chosenHands.values()):
                self.stop()
        else:
            await interaction.response.send_message(content=f"You are not participating in this duel!", ephemeral=True)
        await interactionRespond(interaction)

    @discord.ui.button(label='Rock', style=discord.ButtonStyle.blurple, emoji='🗿')
    async def rockButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button(interaction, button)

    @discord.ui.button(label='Paper', style=discord.ButtonStyle.blurple, emoji='📄')
    async def paperButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button(interaction, button)

    @discord.ui.button(label='Scissors', style=discord.ButtonStyle.blurple, emoji='✂️')
    async def scissorsButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.button(interaction, button)

    async def getHands(self):
        await self.wait()
        return self.chosenHands
      
    def choices(self):
        return self.playerChoices
    


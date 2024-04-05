import discord


async def interactionRespond(interaction: discord.Interaction):
    await interaction.response.defer() if not interaction.response.is_done() else None
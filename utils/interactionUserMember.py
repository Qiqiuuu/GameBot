import discord
def interactionUserMember(interaction: discord.Interaction):
    return interaction.user if interaction.guild is None else interaction.guild.get_member(interaction.user.id)

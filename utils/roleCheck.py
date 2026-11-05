import discord
from discord import app_commands, Interaction

def role_required(role_name: str):
    async def predicate(interaction: Interaction) -> bool:
        if not interaction.guild:
            return False
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role in interaction.user.roles:
            return True
        await interaction.response.send_message("Sorry, you can't do that!", ephemeral=True)
        return False
    return app_commands.check(predicate)
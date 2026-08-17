import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod ready!')

    @app_commands.command()
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "None given :c"):
        await user.kick(reason=reason)
        await interaction.response.send_message(f'Kicked {user} for the following reason: {reason}.', ephemeral=True)

    @app_commands.command()
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "None given :c", delete_message_days: int = 0):
        await user.ban(reason=reason, delete_message_days=delete_message_days)
        await interaction.response.send_message(f'Baned {user} for the following reason: {reason}. Deleted all messages from the past {delete_message_days} days', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot), guilds=[discord.Object(id=1508065145631539281)])
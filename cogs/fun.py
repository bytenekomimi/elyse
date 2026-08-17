from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun loaded!")

    @app_commands.command(name='hiya', description='Say hi!')
    async def hiya(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hiii :3", ephemeral=True)

    @app_commands.command(name='avatar', description='Get an avatar of a user.')
    @app_commands.describe(server_or_global='Choose if you want a server or global/main avatar.')
    async def avatar(self, interaction: discord.Interaction, member: Optional[discord.Member], server_or_global: Literal['Server', 'Global/Main']):
        if member is None:
            member = interaction.user
        if server_or_global == 'Server':
            avatar = member.guild_avatar
        elif server_or_global == 'Global/Main':
            avatar = member.avatar
        await interaction.response.send_message(f"Here's the [avatar]({avatar}) you requested :3", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1508065145631539281)])
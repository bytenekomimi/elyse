import discord, logging
from typing import Literal, Optional
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Fun cog loaded!")

    @app_commands.command(name='avatar', description='Get an avatar of a user.')
    @app_commands.describe(server_or_global='Choose if you want a server or global/main avatar.')
    async def avatar(self, interaction: discord.Interaction, member: Optional[discord.Member], server_or_global: Literal['Server', 'Global/Main']):
        if member is None:
            member = interaction.user
        if server_or_global == 'Server':
            avatar = member.guild_avatar
        elif server_or_global == 'Global/Main':
            avatar = member.avatar
        logger.info(f"Grabbed {avatar} from user{member}, requested by {interaction.user}")
        await interaction.response.send_message(f"Here's the [avatar]({avatar}) you requested :3", ephemeral=True)

    @app_commands.command(name='banner', description='Get the banner of a user.')
    @app_commands.describe(server_or_global='Choose if you want a server or global/main banner.')
    async def banner(self, interaction: discord.Interaction, member: Optional[discord.Member], server_or_global: Literal['Server', 'Global/Main']):
        if member is None:
            member = interaction.user
        if server_or_global == 'Server':
            banner = member.guild_banner
        if server_or_global == 'Global/Main':
            user = await self.bot.fetch_user(member.id)
            banner = user.banner.url
        logger.info(f"Grabbed {banner} from user{member}, requested by {interaction.user}")
        await interaction.response.send_message(f"Here's the [banner]({banner}) you requested :3", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1508065145631539281)])
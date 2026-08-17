import discord, logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Util cog loaded!")

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1508065145631539281)])
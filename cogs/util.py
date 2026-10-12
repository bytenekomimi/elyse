import discord, logging, os, aiohttp
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TSECRET = os.getenv("TBOTSECRET")
TID = os.getenv("TBOTID")
TACCESS = os.getenv("TACCESS")

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

live_bool = False

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_live.start()
        logger.info("Util cog loaded!")

    @tasks.loop(seconds=60)
    async def check_live(self):
        logger.info("Checking live status...")
        params = {"user_login": "byteneko"}
        headers = {"Authorization": f"Bearer {TACCESS}",
                   "Client-Id": TID
                   }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://id.twitch.tv/helix/streams", params=params) as resp:
                global live_bool
                resp.raise_for_status()
                response = await resp.json()
                channel_status = response.get("data", [])
                if channel_status:
                    logger.info("Channel live :)")
                    live_bool = True
                else:
                    logger.info("Channel not live :(")
                    live_bool = False

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1508065145631539281)])
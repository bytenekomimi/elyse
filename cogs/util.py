import asyncio

import discord, logging, os, aiohttp
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from util.twitchAuthCheck import twitchAuthGet, twitchAuthValidate

load_dotenv()

TSECRET = os.getenv("TBOTSECRET")
TID = os.getenv("TBOTID")
TACCESS = os.getenv("TACCESS")
TLIFETIME = int(os.getenv("TLIFETIME") or "0")

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

live_bool = False

async def sendLiveEmbed(self, title: str, category: str, thumbnail_url: str):
    embed = discord.Embed(title="ByteNeko is live now!", color=discord.Color.pink())
    thumbnail = f"{thumbnail_url[:-20]}1920x1080.jpg"
    embed.set_image(url=thumbnail)
    embed.add_field(name="Title", value=title, inline=True)
    embed.add_field(name="Category", value=category, inline=True)
    myguild = self.bot.get_guild(1508065145631539281)
    liveChannel = myguild.get_channel(1564019256134344744)
    await liveChannel.send(embed=embed)

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_live.start()
        self.validate_token.start()
        logger.info("Util cog loaded!")

    @tasks.loop(hours=1)
    async def validate_token(self):
        logger.info("Validating token...")
        await twitchAuthValidate()
        if int(TLIFETIME) <= 600:
            await twitchAuthGet()

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
                    if not live_bool:
                        await sendLiveEmbed(self, title=response['data'][0]['title'], category=response['data'][0]['game_name'] ,thumbnail_url=response['data'][0]['thumbnail_url'])
                        live_bool = True
                    if live_bool:
                        pass
                else:
                    logger.info("Channel not live :(")
                    live_bool = False

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1508065145631539281)])
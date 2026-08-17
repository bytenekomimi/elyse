import discord, os, asyncio, logging
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

GUILD_ID = os.environ['GUILD_ID']
MY_GUILD = discord.Object(id=GUILD_ID)
TOKEN = os.getenv('TOKEN')
LoadedCogs = []
log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)
log_file_name = f"log_date_{datetime.now().strftime('%Y-%m-%d')}_time_{datetime.now().strftime('%H-%M-%S')}.txt"
log_file_path = os.path.join(log_folder, log_file_name)

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=log_file_path)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='$',
                   intents=intents,
                   application_id='1538676052828758086')

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    logger.info(f'Logged in as {bot.user}')

@bot.tree.command(name='sync', description='Synchronize cmds')
async def sync(interaction: discord.Interaction):
    fmt = await bot.tree.sync(guild=MY_GUILD)
    await interaction.response.send_message(f"Refreshed {len(fmt)} commands.", ephemeral=True)

async def loadCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            LoadedCogs.append(filename[:-3])
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await loadCogs()
    await bot.start(TOKEN)

asyncio.run(main())
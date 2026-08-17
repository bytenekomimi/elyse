import discord, os, asyncio

from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.environ['GUILD_ID']
MY_GUILD = discord.Object(id=GUILD_ID)
TOKEN = os.getenv('TOKEN')
LoadedCogs = []

from discord.ext import commands

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
    print(f'Logged in as {bot.user}')

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
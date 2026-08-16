import discord, os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

from discord.ext import commands

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(os.environ['TOKEN'])
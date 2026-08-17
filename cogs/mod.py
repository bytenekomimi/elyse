import discord, logging
from typing import Optional
from discord import app_commands
from discord.ext import commands
logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Mod cog loaded!")

    @app_commands.command()
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "None given :c"):
        await user.kick(reason=reason)

        embed = discord.Embed(title=f"User kicked!", color=discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User", value=f"<@!{user.id}>")
        embed.add_field(name="Performed by", value=f"<@{interaction.user.id}>")
        embed.add_field(name="Reason", value=reason)

        myguild = self.bot.get_guild(1508065145631539281)
        modlog = myguild.get_channel(1539016349580394625)
        await modlog.send(embed=embed)

        logger.info(f"Kicked {user} for \"{reason}\" by {interaction.user}")
        await interaction.response.send_message(f'Kicked {user} for the following reason: {reason}.', ephemeral=True)

    @app_commands.command()
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "None given :c", delete_message_days: int = 0):
        await user.ban(reason=reason, delete_message_days=delete_message_days)

        embed = discord.Embed(title=f"User banned!", color=discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User", value=f"<@!{user.id}>")
        embed.add_field(name="Performed by", value=f"<@{interaction.user.id}>")
        embed.add_field(name="Reason", value=reason)

        myguild = self.bot.get_guild(1508065145631539281)
        modlog = myguild.get_channel(1539016349580394625)
        await modlog.send(embed=embed)

        logger.info(f"Baned {user} for \"{reason}\" by {interaction.user}, with messages deleted for the last {delete_message_days} days.")
        await interaction.response.send_message(f'Baned {user} for the following reason: {reason}. Deleted all messages from the past {delete_message_days} days', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot), guilds=[discord.Object(id=1508065145631539281)])
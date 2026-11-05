import discord
import re
import logging
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


async def fix_pixiv(message: discord.Message, link: str):
    logging.info(f"Found valid pixiv link: {link}")
    link = link.replace("www.", "")
    link = link.replace("pixiv.net", "phixiv.net")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)
    logging.info(f"Fixed pixiv link!")


async def fix_reddit(message: discord.Message, link: str):
    logging.info(f"Found valid reddit link: {link}")
    link = link.replace("www.", "")
    link = link.replace("reddit.com", "vxreddit.com")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)
    logging.info(f"Fixed reddit link!")

async def fix_tiktok(message: discord.Message, link: str):
    logging.info(f"Found valid tiktok link: {link}")
    link = link.replace("www.", "")
    link = link.replace("tiktok.com", "tnktok.com")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)
    logging.info(f"Fixed tiktok link!")


async def fix_twitter(message: discord.Message, link: str):
    logging.info(f"Found valid twitter link: {link}")
    link = link.replace("www.", "")
    link = link.replace("x.com", "twitter.com")
    link = link.replace("twitter.com", "fixvx.com")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)
    logging.info(f"Fixed twitter link!")


class Socialfix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.twitter_pattern = re.compile(r"(https://(www.)?(twitter|x)\.com/[a-zA-Z0-9_]+/status/[0-9]+)")
        self.pixiv_pattern = re.compile(r"(https://(www.)?(pixiv)\.net/en/artworks/[0-9]+)")
        self.reddit_pattern = re.compile(r"(https://(www.)?(reddit)\.com/r/[^/]+/(?:comments|s)/[a-zA-Z0-9]+/?)")
        self.tiktok_pattern = re.compile(r"(https://(www\.)?(tiktok)\.com/[^ \])]+)")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Socialfix cog loaded!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        message_content = message.content.strip("<>")
        if twitter_match := self.twitter_pattern.search(message_content):
            link = twitter_match.group(0)
            await fix_twitter(message, link)
        elif pixiv_match := self.pixiv_pattern.search(message_content):
            link = pixiv_match.group(0)
            await fix_pixiv(message, link)
        elif reddit_match := self.reddit_pattern.search(message.content):
            link = reddit_match.group(0)
            await fix_reddit(message, link)
        elif tiktok_match := self.tiktok_pattern.search(message_content):
            link = tiktok_match.group(0)
            await fix_tiktok(message, link)


async def setup(bot):
    await bot.add_cog(Socialfix(bot), guilds=[discord.Object(id=1508065145631539281)])
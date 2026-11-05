import logging
import random
from datetime import datetime, timezone

import discord
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_cooldowns = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    await self.bot.db.record_join(member)

        logger.info("Levelling cog loaded!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        await self.bot.db.record_join(member)
        logger.info(f"Recorded member join: {member} ({member.id})")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return

        await self.bot.db.record_leave(member)
        logger.info(f"Recorded member leave: {member} ({member.id})")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        member = message.author
        now = datetime.now(timezone.utc).timestamp()
        key = (message.guild.id, member.id)

        last_message = self.xp_cooldowns.get(key, 0)

        #if now - last_message < 10:
        #    return

        self.xp_cooldowns[key] = now
        xp = random.randint(1, 3)

        total_xp, new_level = await self.bot.db.add_xp(
            member, xp
        )

        # Optional: log level-ups for now.
        if new_level > 0:
            row = await self.bot.db.get_member(
                message.guild.id, member.id
            )

            if row is not None and new_level != getattr(
                self, f"_last_level_{message.guild.id}_{member.id}", 0
            ):
                setattr(
                    self,
                    f"_last_level_{message.guild.id}_{member.id}",
                    new_level,
                )
                logger.info(
                    f"{member} reached level {new_level} "
                    f"with {total_xp} XP"
                )


async def setup(bot):
    await bot.add_cog(
        Leveling(bot),
        guilds=[discord.Object(id=1508065145631539281)]
    )

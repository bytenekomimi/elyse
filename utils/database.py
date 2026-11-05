import aiosqlite
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "elyse.db"

class Database:
    def __init__(self, path=DATABASE_PATH):
        self.path = Path(path)
        self.connection = None

    async def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = await aiosqlite.connect(self.path)
        self.connection.row_factory = aiosqlite.Row

        await self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS members (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                joined_at TEXT,
                first_joined_at TEXT,
                last_left_at TEXT,
                total_xp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 0,
                messages INTEGER NOT NULL DEFAULT 0,

                PRIMARY KEY (guild_id, user_id)
            );
        """)

        await self.connection.commit()
        return self

    async def close(self):
        if self.connection is not None:
            await self.connection.close()
            self.connection = None

    async def record_join(self, member):
        now = member.joined_at.isoformat() if member.joined_at else None

        await self.connection.execute("""
            INSERT INTO members (
                guild_id, user_id, username,
                joined_at, first_joined_at, last_left_at
            )
            VALUES (?, ?, ?, ?, ?, NULL)

            ON CONFLICT(guild_id, user_id) DO UPDATE SET
                username = excluded.username,
                joined_at = excluded.joined_at,
                last_left_at = NULL;
        """, (
            member.guild.id,
            member.id,
            member.name,
            now,
            now,
        ))

        await self.connection.commit()

    async def record_leave(self, member):
        await self.connection.execute("""
            UPDATE members
            SET username = ?, last_left_at = ?
            WHERE guild_id = ? AND user_id = ?;
        """, (
            member.name,
            __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ).isoformat(),
            member.guild.id,
            member.id,
        ))

        await self.connection.commit()


    async def add_xp(self, member, amount):
        await self.connection.execute("""
            INSERT INTO members (
                guild_id, user_id, username, total_xp, messages
            )
            VALUES (?, ?, ?, ?, 1)

            ON CONFLICT(guild_id, user_id) DO UPDATE SET
                username = excluded.username,
                total_xp = members.total_xp + excluded.total_xp,
                messages = members.messages + 1;
        """, (
            member.guild.id,
            member.id,
            member.name,
            amount,
        ))

        cursor = await self.connection.execute("""
            SELECT total_xp FROM members
            WHERE guild_id = ? AND user_id = ?;
        """, (member.guild.id, member.id))

        row = await cursor.fetchone()
        total_xp = row["total_xp"]

        # Every 100 * (level + 1)^2 XP thresholds:
        # 100 XP = level 1, 400 XP = level 2, etc.
        level = int((total_xp / 100) ** 0.5)

        await self.connection.execute("""
            UPDATE members SET level = ?
            WHERE guild_id = ? AND user_id = ?;
        """, (level, member.guild.id, member.id))

        await self.connection.commit()
        return total_xp, level


    async def get_member(self, guild_id, user_id):
        cursor = await self.connection.execute("""
            SELECT * FROM members
            WHERE guild_id = ? AND user_id = ?;
        """, (guild_id, user_id))

        return await cursor.fetchone()

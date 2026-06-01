import aiosqlite
from src.config import DATABASE_PATH


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS monitored_repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                owner TEXT NOT NULL,
                repo TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, owner, repo)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS processed_commits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                repo TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(owner, repo, commit_sha)
            )
        """)
        await db.commit()


async def add_repo(chat_id: int, owner: str, repo: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO monitored_repos (chat_id, owner, repo) VALUES (?, ?, ?)",
                (chat_id, owner, repo),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def remove_repo(chat_id: int, owner: str, repo: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM monitored_repos WHERE chat_id = ? AND owner = ? AND repo = ?",
            (chat_id, owner, repo),
        )
        await db.commit()
        return cursor.rowcount > 0


async def list_repos(chat_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT owner, repo, added_at FROM monitored_repos WHERE chat_id = ? ORDER BY added_at DESC",
            (chat_id,),
        )
        return await cursor.fetchall()


async def get_chats_for_repo(owner: str, repo: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT chat_id FROM monitored_repos WHERE owner = ? AND repo = ?",
            (owner, repo),
        )
        return [row[0] for row in await cursor.fetchall()]


async def is_commit_processed(owner: str, repo: str, commit_sha: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM processed_commits WHERE owner = ? AND repo = ? AND commit_sha = ?",
            (owner, repo, commit_sha),
        )
        return await cursor.fetchone() is not None


async def mark_commit_processed(owner: str, repo: str, commit_sha: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            await db.execute(
                "INSERT OR IGNORE INTO processed_commits (owner, repo, commit_sha) VALUES (?, ?, ?)",
                (owner, repo, commit_sha),
            )
            await db.commit()
        except aiosqlite.IntegrityError:
            pass

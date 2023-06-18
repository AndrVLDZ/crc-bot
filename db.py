import aiosqlite


db_name: str = "bot.sqlite"


async def create_table() -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
            await c.execute(
                """
                    CREATE TABLE IF NOT EXISTS users 
                    (id       INT   PRIMARY KEY, 
                    curr_from TEXT, 
                    curr_to   TEXT,
                    round     BOOL);
                    """
            )
        await db.commit()


async def add_user(id: int) -> None:
    # default user configuration
    curr_from: str = "USD"
    curr_to: str = "EUR"
    round: bool = True
    # rows to be added to the database
    rows = ("id", "curr_from", "curr_to", "round")
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
            await c.execute(
                f"""
                INSERT OR REPLACE INTO users {rows} 
                VALUES (?, ?, ?, ?)
                """,
                (id, curr_from, curr_to, round,),
            )
        await db.commit()


async def user_in_db(user_id: int) -> bool:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(
            f"""
            SELECT *
            FROM users 
            WHERE id = ?
            """,
            (user_id,),
        ) as c:
            user_row = await c.fetchone()
            return bool(user_row)  # None = False, tuple = True


async def set_from(user_id: int, currency_from: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
            await c.execute(
                f"""
                UPDATE users 
                SET curr_from = ?
                WHERE id = ?
                """,
                (currency_from, user_id,),
            )
        await db.commit()


async def set_to(user_id: int, currency_to: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
            await c.execute(
                f"""
                UPDATE users 
                SET curr_to = ?
                WHERE id = ?
                """,
                (currency_to, user_id,),
            )
        await db.commit()


async def set_currency_pair(user_id: int, curr_from, curr_to: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
            await c.execute(
                f"""
                UPDATE users 
                SET curr_from = ?,
                    curr_to = ?
                WHERE id = ?
                """,
                (curr_from, curr_to, user_id,),
            )
        await db.commit()


async def set_round_state(user_id: int, round: bool) -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as c:
                await c.execute(
                f"""
                UPDATE users 
                SET round = ?
                WHERE id = ?
                """,
                (round, user_id,),
            )
        await db.commit()


async def get_from(user_id: int) -> str:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(
            f"""
            SELECT curr_from
            FROM users 
            WHERE id = ?
            """,
            (user_id,),
        ) as c:
            result = await c.fetchone()
            if result is None:
                raise IndexError("User does not exist")
            return result[0]


async def get_to(user_id: int) -> str:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(
            f"""
            SELECT curr_to
            FROM users 
            WHERE id = ?
            """,
            (user_id,),
        ) as c:
            result = await c.fetchone()
            if result is None:
                raise IndexError("User does not exist")
            return result[0]


async def get_currency_pair(user_id: int) -> tuple[str, str]:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(
            f"""
            SELECT curr_from, curr_to
            FROM users 
            WHERE id = ?
            """,
            (user_id,),
        ) as c:
            result = await c.fetchone()
            if result is None:
                raise IndexError("User does not exist")
            return result[0], result[1]


async def get_round_state(user_id: int) -> bool:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(
            f"""
            SELECT round
            FROM users 
            WHERE id = ?
            """,
            (user_id,),
        ) as c:
            result = await c.fetchone()
            if result is None:
                raise IndexError("User does not exist")
            return bool(result[0])
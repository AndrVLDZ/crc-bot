import aiosqlite

DB: str = "app/data/db.sqlite"


async def execute_query(query: str, *args) -> None:
    async with aiosqlite.connect(DB) as db:
        async with db.cursor() as cursor:
            await cursor.execute(query, args)
            await db.commit()


async def fetch_query(query: str, *args) -> tuple:
    async with aiosqlite.connect(DB) as db:
        async with db.execute(query, args) as cursor:
            result = await cursor.fetchone()
            return result


async def create_table() -> None:
    query = """
                CREATE TABLE IF NOT EXISTS users
                (id       INT   PRIMARY KEY,
                curr_from TEXT,
                curr_to   TEXT,
                round     BOOL,
                user_data TEXT);
            """
    await execute_query(query)


async def add_user(id: int) -> None:
    # default user configuration
    curr_from: str = "USD 🇺🇸"
    curr_to: str = "EUR 🇪🇺"
    round: bool = True
    user_data: str = ""
    # rows to be added to the database
    rows = ("id", "curr_from", "curr_to", "round", "user_data")
    query = f"""
                INSERT OR REPLACE INTO users {rows}
                VALUES (?, ?, ?, ?, ?)
            """
    await execute_query(query, id, curr_from, curr_to, round, user_data)


async def user_in_db(user_id: int) -> bool:
    query = f"""
                SELECT *
                FROM users
                WHERE id = ?
            """
    user = await fetch_query(query, user_id)
    return bool(user)


async def set_from(user_id: int, currency_from: str) -> None:
    query = f"""
                UPDATE users
                SET curr_from = ?
                WHERE id = ?
            """
    await execute_query(query, currency_from, user_id)


async def set_to(user_id: int, currency_to: str) -> None:
    query = f"""
                UPDATE users
                SET curr_to = ?
                WHERE id = ?
            """
    await execute_query(query, currency_to, user_id)


async def set_currency_pair(user_id: int, curr_from: str, curr_to: str) -> None:
    query = """
                UPDATE users
                SET curr_from = ?,
                    curr_to = ?
                WHERE id = ?
            """
    await execute_query(query, curr_from, curr_to, user_id)


async def set_round_state(user_id: int, round: bool) -> None:
    query = """
                UPDATE users
                SET round = ?
                WHERE id = ?
            """
    await execute_query(query, round, user_id)


async def get_from(user_id: int) -> str:
    query = """
                SELECT curr_from
                FROM users
                WHERE id = ?
            """
    result = await fetch_query(query, user_id)
    return result[0]


async def get_to(user_id: int) -> str:
    query = """
                SELECT curr_to
                FROM users
                WHERE id = ?
            """
    result = await fetch_query(query, user_id)
    return result[0]


async def get_currency_pair(user_id: int) -> tuple[str, str]:
    query = """
                SELECT curr_from, curr_to
                FROM users
                WHERE id = ?
            """
    result = await fetch_query(query, user_id)
    return result[0], result[1]


async def get_round_state(user_id: int) -> bool:
    query = """
                SELECT round
                FROM users
                WHERE id = ?
            """
    result = await fetch_query(query, user_id)
    return bool(result[0])

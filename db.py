import sqlite3

db_name: str = "bot.sqlite"


async def create_table() -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            """
                  CREATE TABLE IF NOT EXISTS users 
                  (id       INT   PRIMARY KEY, 
                  curr_from TEXT, 
                  curr_to   TEXT,
                  round     BOOL);
                  """
        )


async def print_table() -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT * 
                  FROM users
                  """
        )
        records = c.fetchall()
        for row in records:
            print(row)


async def add_user(id: int) -> None:
    # default user configuration
    curr_from: str = "USD"
    curr_to: str = "EUR"
    round: bool = True
    # rows to be added to the database
    rows = ("id", "curr_from", "curr_to", "round")
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  INSERT OR REPLACE INTO users {rows} 
                  VALUES (?, ?, ?, ?)""",
            (id, curr_from, curr_to, round),
        )
        db.commit()


async def check_user_id(user_id: int) -> bool:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT *
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        # fetchone() returns a tuple of values from the table if row exists
        # else - returns None
        user_row = c.fetchone() 
        return bool(user_row) # None = False, tuple = True


async def set_from(user_id: int, currency_from: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET curr_from = ?
                  WHERE id = ?
                  """, (currency_from, user_id)
        )
        try:
            db.commit
        except: 
            raise IndexError("User does not exist")


async def set_to(user_id: int, currency_to: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET curr_to = ?
                  WHERE id = ?
                  """, (currency_to, user_id)
        )
        try:
            db.commit
        except: 
            raise IndexError("User does not exist")

async def set_currency_pair(user_id: int, curr_from, curr_to: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET curr_from = ?,
                      curr_to = ?
                  WHERE id = ?
                  """, (curr_from, curr_to, user_id)
        )
        try:
            db.commit
        except: 
            raise IndexError("User does not exist")

async def set_round_state(user_id: int, round: bool) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET round = ?
                  WHERE id = ?
                  """, (round, user_id)
        )
        try:
            db.commit
        except: 
            raise IndexError("User does not exist")

async def get_from(user_id: int) -> str:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT curr_from
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        try:
            return c.fetchall()[0][0]
        except: 
            raise IndexError("User does not exist")


async def get_to(user_id: int) -> str:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT curr_to
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        
        try: 
            return c.fetchall()[0][0]
        except:
            raise IndexError("User does not exist")


async def get_currency_pair(user_id: int) -> tuple[str, str]:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT curr_from, curr_to
                  FROM users 
                  WHERE id = {user_id}
                  """
        )

        try: 
            x, y = c.fetchall()[0]
            return x, y
        except:
            raise IndexError("User does not exist")


async def get_round_state(user_id: int) -> bool:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT round
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        try: 
            res = bool(c.fetchall()[0][0])
            return res
        except:
            raise IndexError("User does not exist")

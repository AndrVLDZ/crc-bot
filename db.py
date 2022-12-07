import sqlite3

db_name: str = "bot.sqlite"


def create_table() -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            """
                  CREATE TABLE IF NOT EXISTS users 
                  (id       INT   PRIMARY KEY, 
                  name      TEXT, 
                  surname   TEXT, 
                  username  TEXT, 
                  curr_from TEXT  NULL, 
                  curr_to   TEXT  NULL,
                  round     BOOL  TRUE);
                  """
        )


def print_table() -> None:
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


def add_user(id: int, name: str, surname: str, username: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            """
                  INSERT OR REPLACE INTO users (id, name, surname, username) 
                  VALUES (?, ?, ?, ?)""",
            (id, name, surname, username),
        )
        db.commit()


def check_user(user_id: int) -> bool:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT *
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        return bool(c.fetchone())


def set_from(user_id: int, currency_from: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET curr_from = ?
                  WHERE id = ?
                  """, (currency_from, user_id)
        )
        db.commit


def set_to(user_id: int, currency_to: str) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET curr_to = ?
                  WHERE id = ?
                  """, (currency_to, user_id)
        )
        db.commit

def set_round(user_id: int, round: bool) -> None:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  UPDATE users 
                  SET round = ?
                  WHERE id = ?
                  """, (round, user_id)
        )
        db.commit


def get_from(user_id: int) -> str:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT curr_from
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        return c.fetchall()[0][0]


def get_to(user_id: int) -> str:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT curr_to
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        return c.fetchall()[0][0]

def get_round(user_id: int) -> bool:
    with sqlite3.connect(db_name) as db:
        c = db.cursor()
        c.execute(
            f"""
                  SELECT round
                  FROM users 
                  WHERE id = {user_id}
                  """
        )
        return bool(c.fetchall()[0][0])

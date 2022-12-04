import sqlite3 

def create_table() -> None:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()  
            c.execute('''
                  CREATE TABLE IF NOT EXISTS users 
                  (id           INT PRIMARY KEY, 
                  name          TEXT, 
                  surname       TEXT, 
                  username      TEXT, 
                  currency_from TEXT, 
                  currency_to   TEXT);
                  ''')

def print_table() -> None:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  SELECT * 
                  FROM users
                  ''')
            records = c.fetchall()
            for row in records:
                  print(row)

def add_user(id: int, name: str, surname: str, username: str) -> None:
        with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute('''
                  INSERT OR REPLACE INTO users (id, name, surname, username) 
                  VALUES (?, ?, ?, ?)''', (id, name, surname, username))
            db.commit()

def check_user(user_id: int) -> bool:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  SELECT *
                  FROM users 
                  WHERE id = {user_id}
                  ''')
            return bool(c.fetchone())

def set_from(user_id: int, currency_from: str) -> None:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  UPDATE users 
                  SET currency_from = {currency_from}
                  WHERE id = {user_id}
                  ''')
            db.commit

def set_to(user_id: int, currency_to: str) -> None:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  UPDATE users 
                  SET currency_to = {currency_to}
                  WHERE id = {user_id}
                  ''')
            db.commit


def get_from(user_id: int) -> str:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  SELECT currency_from
                  FROM users 
                  WHERE id = {user_id}
                  ''')
            return c.fetchall()[0][0]

def get_to(user_id: int) -> str:
      with sqlite3.connect("bot.db") as db:
            c = db.cursor()
            c.execute(f'''
                  SELECT currency_to
                  FROM users 
                  WHERE id = {user_id}
                  ''')
            return c.fetchall()[0][0]
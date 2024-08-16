import sqlite3
from secrets import token_urlsafe
from user_config import *
from hashlib import sha256

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

user_connection = sqlite3.connect("./database/users.db")
user_cursor = user_connection.cursor()

def init_userdb()->None:
    """
    Create users database.
    """
    user_cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, hashedpassword TEXT, token TEXT)")
    user_cursor.connection.commit()

init_userdb()

def create_admins(username, password)->None:
    """
    create admin user in database and login for website.
    """
    token = token_urlsafe(16)
    user_cursor.execute("INSERT OR IGNORE INTO users (username, hashedpassword, token) VALUES (?, ?, ?)",
                   (username, password, token))
    user_cursor.connection.commit()

for x in users:
    # creates users in database
    create_admins(x[0], sha256(x[1].encode()).hexdigest())
    

if primary_key == None:
    # adds a new column with random token as primary key
    cursor.execute("ALTER TABLE feedback ADD COLUMN id TEXT")
    cursor.connection.commit()
    cursor.execute("UPDATE feedback SET id = ?", (token_urlsafe(5),))
    cursor.connection.commit()

if polarity_column == None:
    cursor.execute("ALTER TABLE feedback ADD COLUMN polarity decimal(1,5)")
    cursor.connection.commit()
    cursor.execute("UPDATE feedback SET polarity = 0")
    cursor.connection.commit()
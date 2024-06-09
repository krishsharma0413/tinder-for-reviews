import sqlite3
from secrets import token_urlsafe

DATABASE_PATH = './database/feedback.db'
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


def create_admins(username, password)->None:
    """
    create admin user in database and login for website.
    """
    token = token_urlsafe(16)
    cursor.execute("INSERT INTO users (username, hashedpassword, token) VALUES (?, ?, ?)",
                   (username, password, token))
    cursor.connection.commit()

# create_admins("admin", sha256("admin".encode()).hexdigest())


def create_fake_data()->None:
    """
    Create 10,000 fake data entry in database for testing purposes.
    """
    for x in range(10000):
        token = token_urlsafe(5)
        cursor.execute("INSERT INTO feedback (id, review_content, positive,\
            negative, neutral, polarity) VALUES (?, ?, ?, ?, ?, ?)",
                       (token, "This is a review", 0, 0, 0, 0))
        cursor.execute("INSERT INTO postinformation\
            (id, creation, link, source) VALUES (?, ?, ?, ?)",
                       (x, "2021-09-01", "https://www.google.com", "Google"))
    cursor.connection.commit()

# create_fake_data()
import unittest
from config import user_cursor

class TestLogin(unittest.TestCase):
    
    def test_db(self):
        user_cursor.execute("SELECT * FROM users")
        result = user_cursor.fetchone()
        self.assertIsNotNone(result, msg="MISSING USERS : No user found in database. You won't be able to login.")



if __name__ == "__main__":
    unittest.main()
import unittest
from user_config import *
from config import cursor
from os import path

class TestDatabase(unittest.TestCase):
    
    def test_db_path(self):
            self.assertTrue(path.exists(DATABASE_PATH), msg=f"INCORECT PATH : Database not found on the given path {DATABASE_PATH}.")
                
    def test_columns(self):
        try:
            cursor.execute(f"SELECT {left_swipe[0]}, {right_swipe[0]}, {up_swipe[0]} FROM {table_name}")
            self.assertTrue(1, msg="MISSING COLUMNS : One or more columns are missing from the users table.")
        except Exception as e:
            self.fail(f"Error: {e}")


if __name__ == "__main__":
    unittest.main()
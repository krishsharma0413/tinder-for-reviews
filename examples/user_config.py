"""
author: krishsharma0413

This file is to setup your tinder-for-reviews in a more user-friendly manner.
"""

table_name = "feedback"
primary_key = "id" # primary key of your database. If None, it will be auto generated.
DATABASE_PATH = './demoDB/feedback.db'

# what all columns/headers does your sql data have?
headers = ["id", "review_content", "positive",
           "negative", "neutral", "polarity"]


# which column/header do you want to be shown on the review card?
column_for_review = "review_content"
review_type = "text" # options: "text" (support for image, videos soon)
polarity_column = "polarity" # if set to None, a new column will be created with the name "polarity"

# what does each swipe add value to? please make sure these columns are int
# polarity wise, right is positive (+1), up is neutral (+0), and left is negative (-1)
left_swipe = ["negative", "negative"] # [column name, display name (label on the website)]
up_swipe = ["neutral", "neu"] # [column name, display name (label on the website)]
right_swipe = ["positive", "positive"] # [column name, display name (label on the website)]

# A list of tuple which has username and then password
users = [("admin", "admin")]

# setup host here for the server.
# future tests might require the testcase to run the server
# so to make sure it runs on the same host, you can set it up here.
host = "localhost"
port = 5556
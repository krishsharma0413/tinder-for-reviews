# 🔥Tinder for Reviews

Tired of labelling your dataset *the boring way*? Introducing **Tinder for Reviews**.
Now label your dataset as if you are scrolling on tinder!

## Demo

A demo of how the works.


[![Watch the video](https://github.com/krishsharma0413/tinder-for-reviews/assets/77439837/7d9f1516-1e25-47bf-8ca1-263d343c02ab)](https://github.com/krishsharma0413/tinder-for-reviews/assets/77439837/c00c0036-6d48-4b45-893b-ad763cdc7a17)


## Installation

```bash
pip install -r requirements.txt
```

## Setup
1. Save your SQLite database in `database` folder and go through `user_config.py` and setup your SQLite database accordingly.

An example **user_config.py** with headers such as `["id", "review_content", "positive", "negative", "neutral", "polarity"]` has been added to [examples/user_config.py](/examples/user_config.py) along with a demo database at `demoDB/feedback.db`

```py
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
```

## Usage
```bash
python main.py
```
and open `http://localhost:5556` (or your custom host) in your browser.

- right swipes or green button = positive*.
- left swipe or red button = negative*.
- white button "neu" = neutral*.

\*  or whatever you have configured in `user_config.py`

## Running Tests
Run tests using `pytest` on your terminal.
```terminal
pytest --verbose -s
```

## Usecase

You can use this to label your dataset for sentiment analysis, feedback analysis, etc in a fun way. Well, that's what I am using this for :P
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
1. Please save your `.db` database with it's name in `database` folder and go through `user_config.py` and setup your SQLite database accordingly.

An example **SQLite database** with headers such as `["id", "review_content", "positive", "negative", "neutral", "polarity"]` would look like.

```py
"""
author: krish sharma

This file is to setup your tinder-for-reviews without much difficulties.

For review_type = "image". Please make sure that it is TEXT data type
and has either "relative path" of the images or BASE64 image data.
"""

DATABASE_PATH = "./database/feedback.db" # this is an example database.

# what all columns/headers does your sql data have?
headers = ["id", "review_content", "positive",
           "negative", "neutral", "polarity"]


# which column/header do you want to be shown on the review card?
column_for_review = "review_content"
review_type = "text" # options: "text" or "image" (support for videos soon)
polarity_column = "polarity"

# what does each swipe add value to? please make sure these columns are int
# ["column name", "name showed on website buttons."]
left_swipe = ["negative", "negative"]
up_swipe = ["neutral", "neu"]
right_swipe = ["positive", "positive"]
```

You can also use for feedback and postinformation tables yourself to add the data you like and configure this **example database**.
```sql
INSERT INTO feedback (id, review_content, positive, negative, neutral, polarity) VALUES (?, ?, ?, ?, ?, ?)

INSERT INTO postinformation (id, creation, link, source) VALUES (?, ?, ?, ?)
```

## Usage
```bash
python main.py
```
and open `http://localhost:8000` in your browser.

- right swipes or green button = positive*.
- left swipe or red button = negative*.
- white button "neu" = neutral*.

\*  or whatever you have configured in `user_config.py`
## Usecase

You can use this to label your dataset for sentiment analysis, feedback analysis, etc in a fun way. Well, that's what I am using this for :P
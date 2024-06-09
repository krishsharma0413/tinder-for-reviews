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
1. line `33` in `app.py` creates a user with the username `admin` and password `admin`. Change this to your desired username and password.
2. line `42` in `app.py` creates sample data for 10k reviews.

You can also use for feedback and postinformation tables yourself to add the data you like and configure the database.
```sql
INSERT INTO feedback (id, review_content, positive, negative, neutral, polarity) VALUES (?, ?, ?, ?, ?, ?)

INSERT INTO postinformation (id, creation, link, source) VALUES (?, ?, ?, ?)
```

## Usage
```bash
python main.py
```
and open `http://localhost:8000` in your browser.

- right swipes or green button = positive.
- left swipe or red button = negative
- white button "neu" = neutral

`Usecase: You can use this to label your dataset for sentiment analysis, feedback analysis, etc in a fun way.`

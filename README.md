# 🔥Tinder for Reviews

Tired of labelling your dataset *the boring way*? Introducing **Tinder for Reviews**

## Demo

A demo of how the works.
<video width="320" height="240" controls>
  <source src="./static/2024-06-07_21-31-08.mov" type="video/mp4">
</video>

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

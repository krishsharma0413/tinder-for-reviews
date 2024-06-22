"""
author: krish sharma

This file is to setup your tinder-for-reviews without much difficulties.

For review_type = "image". Please make sure that it is TEXT data type
and has either "relative path" of the images or BASE64 image data.
"""

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
#print("hello this is an imposter syndrome detection tool")
import praw
import csv
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import numpy as np
import os

password = os.getenv("REDDIT_PASSWORD")
reddit = praw.Reddit(
    client_id="3p3gEZnTy7BBL5r_vU7d5g",
    client_secret="b0cq6mQivbpq8hUpvUbNW1aimh03bg",
    user_agent="RedditScraper by u/saudamini_79",
    username="saudamini_79",
    password=password
)

print("Authentication successful:", reddit.user.me())

subreddit = reddit.subreddit("impostersyndrome")

'''for post in subreddit.hot(limit=1):
    print(f"Title: {post.title}")
    print(f"Score: {post.score}")
    print(f"URL: {post.url}")
    print("-" * 50)'''

for post in subreddit.search("imposter syndrome", limit=1):
    print(f"Title: {post.title} | Score: {post.score} | ID: {post.author} | URL: {post.url}") 

with open("reddit_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f) 
    writer.writerow(["Title", "Score", "URL","Selftext"])
    for post in subreddit.hot(limit=10): 
        writer.writerow([post.title, post.score, post.url, post.selftext])

df = pd.read_csv("reddit_posts.csv")
df = df.dropna(subset=["Selftext"])
df["text"] = df["Selftext"].astype(str)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-z\s]", "", text)  # remove punctuation/numbers
    return text

df["clean_text"] = df["text"].apply(clean_text)
df.to_csv("reddit_posts.csv", index=False, encoding="utf-8")
print(df.head())
df["label"] = np.random.randint(0, 2, df.shape[0])
df.to_csv("reddit_posts.csv", index=False, encoding="utf-8")


X = df["clean_text"]
y = df["label"]   # make sure you have this column!

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train
clf = LogisticRegression()
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))
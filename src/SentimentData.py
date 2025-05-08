import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from datetime import datetime
from RedditPost import RedditPost

nltk.download("vader_lexicon")

class SentimentData:
    def __init__(self, keyword, start_date, end_date, limit=50):
        self.keyword = keyword
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.limit = limit
        self.posts = []
        self.scores = []

        self.reddit = praw.Reddit(
            client_id="0Jj0eBOFynB-Q687cImBNQ",
            client_secret="Wj_8-9I1Txaco5-2DJOAuEAC1QMwjw",
            user_agent="crypto_sentiment_app by /u/Sad-Ad2335"
        )

        self.sid = SentimentIntensityAnalyzer()

    def fetch_posts(self):
        subreddit = self.reddit.subreddit("CryptoCurrency")
        results = subreddit.search(self.keyword, sort="new", limit=self.limit)

        for post in results:
            post_date = datetime.utcfromtimestamp(post.created_utc)
            if self.start_date <= post_date <= self.end_date:
                text = post.title + " " + post.selftext
                self.posts.append(RedditPost(text, post_date, 0))

    def analyze_sentiment(self):
        for post in self.posts:
            score = self.sid.polarity_scores(post.text)["compound"]
            post.score = score
            self.scores.append(score)

    def get_extremes(self):
        sorted_posts = sorted(self.posts, key=lambda x: x.score)
        return sorted_posts[-5:], sorted_posts[:5]

    def to_dataframe(self):
        return pd.DataFrame([
            {"date": p.date, "text": p.text, "sentiment": p.score}
            for p in self.posts
        ])

    def get_average_score(self):
        return round(sum(self.scores) / len(self.scores), 4) if self.scores else 0.0
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from datetime import datetime

nltk.download("vader_lexicon")

class SentimentData:
    def __init__(self, keyword, limit=50):
        self.keyword = keyword
        self.limit = limit
        self.posts = []
        self.scores = []

        # Reddit credentials — make sure you set these up at reddit.com/prefs/apps
        self.reddit = praw.Reddit(
            client_id="0Jj0eBOFynB-Q687cImBNQ",
            client_secret="Wj_8-9I1Txaco5-2DJOAuEAC1QMwjw",
            user_agent="crypto_sentiment_app by /u/Sad-Ad2335"
        )

        self.sid = SentimentIntensityAnalyzer()

    def fetch_posts(self):
        subreddit = self.reddit.subreddit("CryptoCurrency")
        results = subreddit.search(self.keyword, limit=self.limit)

        for post in results:
            text = post.title + " " + post.selftext
            date = datetime.utcfromtimestamp(post.created_utc)
            self.posts.append({"text": text, "date": date})

    def analyze_sentiment(self):
        for post in self.posts:
            score = self.sid.polarity_scores(post["text"])["compound"]
            post["sentiment"] = score
            self.scores.append(score)

    def to_dataframe(self):
        return pd.DataFrame(self.posts)

    def get_average_sentiment(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0

    
#sentiment = SentimentData("bitcoin", limit=50)
#sentiment.fetch_posts()
#sentiment.analyze_sentiment()

#df = sentiment.to_dataframe()
#print(df.head())
#print("Average sentiment score:", sentiment.get_average_sentiment())
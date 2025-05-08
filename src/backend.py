import os
import requests
from CryptoData import CryptoData
from SentimentData import SentimentData
from DataAnalyzer import DataAnalyzer
from OpenAISummarizer import OpenAISummarizer
from pathlib import Path

price_csv = Path("data/price_metrics.csv")
sentiment_csv = Path("data/sentiment_analysis.csv")


def fetch_full_analysis(crypto, start_date, end_date):
    try:
        for f in [price_csv, sentiment_csv]:
            if f.exists():
                f.unlink()

        crypto_fetcher = CryptoData(crypto, start_date, end_date)
        price_df = crypto_fetcher.fetch_data()

        if price_df.empty:
            return None, "No price data available.", ""

        sentiment_fetcher = SentimentData(crypto, start_date, end_date, limit=50)
        sentiment_fetcher.fetch_posts()
        sentiment_fetcher.analyze_sentiment()

        top5, bottom5 = sentiment_fetcher.get_extremes()
        all_text = [p.text for p in sentiment_fetcher.posts]

        try:
            summary = summarizer.summarize(all_text)
        except Exception as e:
            summary = f"GPT Summary unavailable: {e}"

        average_score = sentiment_fetcher.get_average_score()

        analyzer = DataAnalyzer(price_df, sentiment_fetcher.to_dataframe())
        analyzer.run_full_analysis()
        analyzer.save_metrics_csv(price_csv)
        analyzer.save_sentiment_csv(sentiment_csv, top5, bottom5)

        sentiment_output = "Sentiment Analysis (using Reddit post scores from VADER):\n"
        sentiment_output += f"Score: {average_score}\n\n"
        sentiment_output += "Top 5 Positive Posts:\n"
        for post in top5:
            sentiment_output += f"{post.date}: {post.text}\n\n"
        sentiment_output += "Bottom 5 Negative Posts:\n"
        for post in bottom5:
            sentiment_output += f"{post.date}: {post.text}\n\n"

        return analyzer.get_result(), summary, sentiment_output
    except Exception as e:
        return None, f"Error: {str(e)}", ""

def fetch_marketcap_and_trending(crypto):
    base = "https://api.coingecko.com/api/v3"
    try:
        coin = requests.get(f"{base}/coins/{crypto.lower()}").json()
        marketcap = coin.get("market_data", {}).get("market_cap", {}).get("usd", "N/A")

        trending = requests.get(f"{base}/search/trending").json()
        top_coins = [item['item']['name'] for item in trending.get("coins", [])[:5]]
        return marketcap, top_coins
    except Exception:
        return "N/A", []
def cleanup_data_files():
    for f in [price_csv, sentiment_csv]:
        if f.exists():
            f.unlink()
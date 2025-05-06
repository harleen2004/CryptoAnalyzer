import pandas as pd
from datetime import datetime
import os

class DataAnalyzer:
    def __init__(self, price_df, sentiment_df=None):
        self.price_df = price_df.copy()
        self.sentiment_df = sentiment_df.copy() if sentiment_df is not None else None
        self.merged_df = pd.DataFrame()

    def compute_daily_returns(self):
        self.price_df["returns"] = self.price_df["price"].pct_change()

    def compute_moving_average(self, window=7):
        self.price_df[f"ma_{window}"] = self.price_df["price"].rolling(window=window).mean()

    def compute_volatility(self, window=7):
        if "returns" not in self.price_df.columns:
            self.compute_daily_returns()
        self.price_df[f"vol_{window}"] = self.price_df["returns"].rolling(window=window).std()

    def process_sentiment(self):
        if self.sentiment_df is not None and not self.sentiment_df.empty:
            self.sentiment_df["date"] = pd.to_datetime(self.sentiment_df["date"]).dt.date
            self.sentiment_df = self.sentiment_df[self.sentiment_df["sentiment"].notna()]
            self.sentiment_df["sentiment"] = self.sentiment_df["sentiment"].astype(float)
            sentiment_grouped = self.sentiment_df.groupby("date", as_index=False)["sentiment"].mean()
            sentiment_grouped.rename(columns={"sentiment": "avg_sentiment"}, inplace=True)
            self.sentiment_df = sentiment_grouped

    def merge_data(self):
        self.price_df["date"] = pd.to_datetime(self.price_df["date"]).dt.date
        self.merged_df = self.price_df.copy()
        # Merge sentiment only for internal calculations — not saving avg_sentiment in CSV
        if self.sentiment_df is not None:
            merged_temp = pd.merge(self.price_df, self.sentiment_df, on="date", how="left")
            merged_temp.dropna(subset=["price"], inplace=True)
            self.merged_df = merged_temp.drop(columns=["avg_sentiment"], errors="ignore")

    def run_full_analysis(self):
        self.compute_daily_returns()
        self.compute_moving_average(7)
        self.compute_moving_average(30)
        self.compute_volatility(7)
        if self.sentiment_df is not None:
            self.process_sentiment()
        self.merge_data()

    def get_result(self):
        return self.merged_df

    def filter_by_date_range(self, start_date, end_date):
        if self.merged_df.empty:
            print("Merged data is empty. Run analysis first.")
            return pd.DataFrame()
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        return self.merged_df[(self.merged_df["date"] >= start) & (self.merged_df["date"] <= end)]

    def get_average_sentiment_in_range(self, start_date, end_date):
        if self.sentiment_df is None or self.sentiment_df.empty:
            return None
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        filtered = self.sentiment_df[
            (self.sentiment_df["date"] >= start) &
            (self.sentiment_df["date"] <= end)
        ]
        if filtered.empty:
            return None
        return filtered["avg_sentiment"].mean()
    

    def save_result_csv(self, filename="merged_crypto_sentiment.csv", folder="data"):
        if self.merged_df.empty:
            print("No data to save.")
            return
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        self.get_result().to_csv(path, index=False)
        print(f"Saved full analysis to: {path}")

    def save_filtered_csv(self, start_date, end_date, filename="filtered_crypto_sentiment.csv", folder="data"):
        filtered = self.filter_by_date_range(start_date, end_date)
        if filtered.empty:
            print("No filtered data to save.")
            return
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        filtered.to_csv(path, index=False)
        print(f"Saved filtered analysis to: {path}")

import pandas as pd
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
            sentiment_grouped = self.sentiment_df.groupby("date").mean(numeric_only=True).reset_index()
            sentiment_grouped.rename(columns={"sentiment": "avg_sentiment"}, inplace=True)
            self.sentiment_df = sentiment_grouped

    def merge_data(self):
        self.price_df["date"] = pd.to_datetime(self.price_df["date"]).dt.date
        self.merged_df = self.price_df.copy()

        if self.sentiment_df is not None:
            self.merged_df = pd.merge(self.price_df, self.sentiment_df, on="date", how="left")

        self.merged_df = self.merged_df[self.merged_df["price"].notna()]

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

    def save_metrics_csv(self, path):
        self.merged_df.to_csv(path, index=False)

    def save_sentiment_csv(self, path, top5, bottom5):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Top 5 Positive Posts:\n")
            for post in top5:
                f.write(f"{post}\n")
            f.write("\nBottom 5 Negative Posts:\n")
            for post in bottom5:
                f.write(f"{post}\n")
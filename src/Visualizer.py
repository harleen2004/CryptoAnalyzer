import pandas as pd
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, csv_path):
        try:
            self.df = pd.read_csv(csv_path)
            self.df["date"] = pd.to_datetime(self.df["date"])
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
            self.df = pd.DataFrame()

    def plot_price(self):
        if self.df.empty:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.df["date"], self.df["price"], label="Price", color="blue")
        plt.title("Bitcoin Price Over Time")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_moving_averages(self):
        if self.df.empty or "ma_7" not in self.df.columns or "ma_30" not in self.df.columns:
            print("Moving average data not found.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.df["date"], self.df["price"], label="Price", alpha=0.5)
        plt.plot(self.df["date"], self.df["ma_7"], label="7-Day MA", linestyle="--")
        plt.plot(self.df["date"], self.df["ma_30"], label="30-Day MA", linestyle=":")
        plt.title("Bitcoin Price and Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_volatility(self):
        if self.df.empty or "vol_7" not in self.df.columns:
            print("Volatility data not found.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.df["date"], self.df["vol_7"], label="7-Day Volatility", color="purple")
        plt.title("Bitcoin Volatility (7-Day Rolling Std Dev of Returns)")
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_all(self):
        if self.df.empty:
            print("No data to plot.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(self.df["date"], self.df["price"], label="Price", alpha=0.6)
        if "ma_7" in self.df.columns:
            plt.plot(self.df["date"], self.df["ma_7"], label="7-Day MA", linestyle="--")
        if "ma_30" in self.df.columns:
            plt.plot(self.df["date"], self.df["ma_30"], label="30-Day MA", linestyle=":")
        if "vol_7" in self.df.columns:
            plt.plot(self.df["date"], self.df["vol_7"], label="Volatility", linestyle="-.", color="purple")
        plt.title("Bitcoin Price, Moving Averages, and Volatility")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

viz = Visualizer("../data/filtered_crypto_sentiment.csv")
#viz.plot_price()
#viz.plot_moving_averages()
#viz.plot_volatility()
viz.plot_all()
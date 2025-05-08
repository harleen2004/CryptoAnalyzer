import requests
import pandas as pd
from datetime import datetime

class CryptoData:
    def __init__(self, coin_id, start_date, end_date):
        self.coin_id = coin_id.lower()  # e.g., 'bitcoin'
        self.start_date = start_date
        self.end_date = end_date
        self.df = pd.DataFrame()

    
    def fetch_data(self):
        from_ts = int(datetime.strptime(self.start_date, "%Y-%m-%d").timestamp())
        to_ts = int(datetime.strptime(self.end_date, "%Y-%m-%d").timestamp())

        url = (
            f"https://api.coingecko.com/api/v3/coins/{self.coin_id}/market_chart/range"
            f"?vs_currency=usd&from={from_ts}&to={to_ts}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; CryptoSentimentApp/1.0; +https://example.com)"
        }

        print("Fetching from:", url)

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return pd.DataFrame()

        data = response.json()
        prices = data.get("prices", [])

        if not prices:
            print("No price data found!")
            return pd.DataFrame()

        self.df = pd.DataFrame(prices, columns=["timestamp", "price"])
        self.df["date"] = pd.to_datetime(self.df["timestamp"], unit="ms")
        self.df = self.df[["date", "price"]]
        return self.df



    def save_to_csv(self, filename):
        self.df.to_csv(filename, index=False)



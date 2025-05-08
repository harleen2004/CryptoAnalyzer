from CryptoData import CryptoData
from SentimentData import SentimentData
from DataAnalyzer import DataAnalyzer
from datetime import datetime, timedelta

def main():
    # Step 1: Define user date range (for both price and sentiment)
    end = datetime.today()
    start = end - timedelta(days=30)
    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    print(f"Fetching data from {start_date} to {end_date}...")

    # Step 2: Fetch crypto price data
    btc = CryptoData("bitcoin", start_date, end_date)
    price_df = btc.fetch_data()

    if price_df is None or price_df.empty:
        print("Failed to fetch price data. Exiting.")
        return

    # Step 3: Fetch Reddit sentiment data
    sentiment = SentimentData("bitcoin", limit=50)
    sentiment.fetch_posts()
    sentiment.analyze_sentiment()
    sentiment_df = sentiment.to_dataframe()

    # Step 4: Analyze and process data
    analyzer = DataAnalyzer(price_df, sentiment_df)
    analyzer.run_full_analysis()

    # Step 5: Save full merged CSV
    analyzer.save_result_csv()  # data/merged_crypto_sentiment.csv

    # Step 6: Save filtered data (same as user-specified range)
    analyzer.save_filtered_csv(start_date, end_date)

    # Step 7: Get average sentiment for the same range
    avg_sentiment = analyzer.get_average_sentiment_in_range(start_date, end_date)
    if avg_sentiment is not None:
        print(f"Average sentiment from {start_date} to {end_date}: {avg_sentiment:.4f}")
    else:
        print(f"No sentiment data found from {start_date} to {end_date}.")

if __name__ == "__main__":
    main()

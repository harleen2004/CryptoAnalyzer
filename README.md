
# CryptoAnalyzer
Harleen Sandhu
This project is a Python-based cryptocurrency analysis tool that allows users to fetch, analyze, and visualize historical price data alongside public sentiment. Using a graphical user interface built with Tkinter, users can select a cryptocurrency, define a date range, and view detailed charts of price trends, moving averages, and volatility. The application integrates real-time Reddit data and performs sentiment analysis using VADER to examine the relationship between market sentiment and price behavior. The backend is designed using object oriented programming principles for modularity, readability, and reusability. This tool demonstrates the integration of financial data analytics, as well as some machine learning topics to give better analysis of the state of cryptocurrencies and how public opinion plays a role. 
 
 
CryptoAnalyzer is a Python-based application that collects, analyzes, and visualizes real-time cryptocurrency price data alongside social media sentiment trends. It integrates the CoinGecko API for fetching historical price data and Reddit’s r/CryptoCurrency subreddit for sentiment extraction using natural language processing. The goal is to evaluate how market sentiment correlates with price fluctuations and volatility over time. The user interface allows users to select a date range, run an analysis, and view price trends, moving averages, and volatility plots. The application is built with modular, object-oriented design principles and is fully reproducible using a Conda environment.

PROJECT OUTLINE:
Set up data collection classes for price and sentiment.

Build a data analysis engine to compute technical indicators and merge datasets.

Design a visualization module for plotting price trends, moving averages, and volatility.

Implement a Tkinter GUI to allow user input, initiate analysis, and display results.

Test all components and document the project in GitHub with usage instructions.

INTERFACE PLAN
The interface is built using Python’s Tkinter library. It contains:

A home screen with input fields for start and end date.

A button to fetch and analyze data for Bitcoin.

Output areas for average sentiment and technical metric summaries.

Buttons to display different plots using the Visualizer module.

At least four widgets including input fields, buttons, and labels across two windows.

DATA COLLECTION:
The project collects Bitcoin price data using the CoinGecko API and cryptocurrency-related posts from Reddit using the PRAW library. The collected data is stored locally in the data/ directory. Merged and filtered datasets are saved as CSV files using built-in pandas methods, and the DataAnalyzer class handles all saving to ensure modularity. All API access is rate-limited and adheres to public access guidelines. The data is structured with timestamped price entries and grouped sentiment scores, prepared for time-series analysis.

DATA ANALYSIS:
The DataAnalyzer class computes daily returns, moving averages, and rolling volatility from the price data. It also processes Reddit sentiment data using VADER to extract compound sentiment scores, grouping them by date. The final merged dataset is used for trend visualization through the Visualizer class, which plots price over time, moving averages, and volatility. Sentiment is summarized numerically for the selected time period and displayed in the UI. Visualization is handled with matplotlib to produce clear, labeled charts on demand.



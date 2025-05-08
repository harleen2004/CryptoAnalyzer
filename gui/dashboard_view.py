
# Directory: CryptoAnalyzer/gui/dashboard_view.py
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import fetch_full_analysis, fetch_marketcap_and_trending, cleanup_data_files

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, crypto, start, end, back_callback):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.crypto = crypto
        self.start = start
        self.end = end
        self.back_callback = back_callback

        self.sidebar_frame = ctk.CTkFrame(self, width=300)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.update_data()

    def update_data(self):
        df, summary, sentiment_output = fetch_full_analysis(self.crypto, self.start, self.end)

        if df is None:
            messagebox.showerror("Error", summary)
            self.back_callback()
            return

        marketcap, trending = fetch_marketcap_and_trending(self.crypto)

        # Create the plots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), constrained_layout=True)
        ax1.plot(df["date"], df["price"], label="Price")
        ax1.plot(df["date"], df["ma_7"], label="MA 7")
        ax1.legend()
        ax1.set_title(f"{self.crypto} Price & Moving Average\nMarket Cap: ${marketcap:,}")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price (USD)")
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()

        ax2.plot(df["date"], df["vol_7"], label="Volatility", color='orange')
        ax2.set_title("Volatility")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Volatility")
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Sentiment Section
        sentiment_section = ctk.CTkFrame(self.sidebar_frame)
        sentiment_section.pack(pady=10, padx=10, fill="both", expand=False)

        sentiment_title = ctk.CTkLabel(sentiment_section, text="Sentiment Analysis", font=("Arial", 16, "bold"))
        sentiment_title.pack(pady=(10, 5))

        self.sentiment_label = ctk.CTkTextbox(sentiment_section, width=280, height=300, wrap="word")
        self.sentiment_label.pack(padx=5, pady=5, fill="both", expand=True)
        self.sentiment_label.insert("0.0", sentiment_output)
        self.sentiment_label.configure(state="disabled")

        # Trending Section
        trending_title = ctk.CTkLabel(self.sidebar_frame, text="Trending Cryptos", font=("Arial", 14, "bold"))
        trending_title.pack(pady=(15, 5))

        self.trending_box = ctk.CTkTextbox(self.sidebar_frame, width=280, height=80)
        self.trending_box.pack(padx=5, pady=5)
        self.trending_box.insert("0.0", "Top Trending: " + ", ".join(trending))
        self.trending_box.configure(state="disabled")

        # GPT Summary Box
        summary_title = ctk.CTkLabel(self.sidebar_frame, text="GPT Summary", font=("Arial", 14, "bold"))
        summary_title.pack(pady=(15, 5))

        self.summary_box = ctk.CTkTextbox(self.sidebar_frame, width=280, height=100, wrap="word")
        self.summary_box.pack(padx=5, pady=5)
        self.summary_box.insert("0.0", summary)
        self.summary_box.configure(state="disabled")

        # Back Button
        back_button = ctk.CTkButton(self.sidebar_frame, text="Back", command=self.on_back)
        back_button.pack(pady=20)

    def on_back(self):
        cleanup_data_files()
        self.back_callback()

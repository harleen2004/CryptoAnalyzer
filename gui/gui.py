import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import customtkinter as ctk
from home_view import HomeView
from dashboard_view import DashboardView
from backend import fetch_full_analysis, fetch_marketcap_and_trending, cleanup_data_files
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CryptoAnalyzer")
        self.geometry("1000x700")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.frame = None
        self.show_home()

    def show_home(self):
        if self.frame:
            self.frame.destroy()
        self.frame = HomeView(self, self.show_dashboard)
        self.frame.pack(fill="both", expand=True)

    def show_dashboard(self, crypto, start, end):
        if self.frame:
            self.frame.destroy()
        self.frame = DashboardView(self, crypto, start, end, self.show_home)
        self.frame.pack(fill="both", expand=True)

    def on_close(self):
        from backend import cleanup_data_files
        cleanup_data_files()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()


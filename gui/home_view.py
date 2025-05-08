import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

class HomeView(ctk.CTkFrame):
    def __init__(self, master, switch_to_dashboard):
        super().__init__(master)
        self.switch_to_dashboard = switch_to_dashboard

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="CryptoAnalyzer", font=("Arial", 24)).pack(pady=20)

        self.crypto_entry = ctk.CTkEntry(self, placeholder_text="Enter cryptocurrency (e.g., bitcoin)")
        self.crypto_entry.pack(pady=10)

        self.start_date = DateEntry(self, width=16, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.pack(pady=10)

        self.end_date = DateEntry(self, width=16, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="Analyze", command=self.launch_dashboard)
        self.start_btn.pack(pady=20)

    def launch_dashboard(self):
        crypto = self.crypto_entry.get().strip()
        start = self.start_date.get_date().strftime("%Y-%m-%d")
        end = self.end_date.get_date().strftime("%Y-%m-%d")

        if not crypto:
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        self.switch_to_dashboard(crypto, start, end)
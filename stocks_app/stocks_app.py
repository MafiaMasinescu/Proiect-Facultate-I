import datetime
from dateutil.relativedelta import relativedelta
from tiingo import TiingoClient
import matplotlib.pyplot as plt
from matplotlib import style
import customtkinter as ctk
import tkinter.messagebox as messagebox

class StockTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.all_tickers = []
        self.dates_string = ""
        self.tickers_string = ""
        
        self.one_year_ago = datetime.datetime.now() - relativedelta(years=1)
        self.six_months_ago = datetime.datetime.now() - relativedelta(months=6)
        self.one_month_ago = datetime.datetime.now() - relativedelta(months=1)
        self.one_day_ago = datetime.datetime.now() - relativedelta(days=1)
        self.one_hour_ago = datetime.datetime.now() - relativedelta(hours=1)
        self.custom_date = datetime.datetime.now() - relativedelta(months=1)
        
        self.config = {
            'session': True,
            'api_key': 'dfb9f93dbad1265cd752e91b04bfad36e0c870f4'
        }

        self.client = TiingoClient(self.config)    
        self.title("Stock Performance Tracker")
        self.geometry("400x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Stock Performance Tracker",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=10)
        self.period_label = ctk.CTkLabel(
            self.main_frame,
            text="Select Period:",
            font=("Helvetica", 16)
        )

        self.period_label.pack(pady=5)        
        self.period_var = ctk.StringVar(value="Six Months")
        self.period_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["One Hour", "One Day", "One Month", "Six Months", "One Year", "All Time"],
            variable=self.period_var
        )
        self.period_menu.pack(pady=5)
        self.ticker_label = ctk.CTkLabel(
            self.main_frame,
            text="Stock Ticker:",
            font=("Helvetica", 16)
        )
        self.ticker_label.pack(pady=5)
        
        self.ticker_input = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter ticker symbol..."
        )
        self.ticker_input.pack(pady=5)        
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        self.plot_button = ctk.CTkButton(
            self.button_frame,
            text="Plot Stock",
            command=self.plot_stock
        )
        self.plot_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear Chart",
            command=self.clear_chart
        )
        self.clear_button.pack(side="left", padx=5)
        
        self.stocks_label = ctk.CTkLabel(
            self.main_frame,
            text="Currently plotted stocks: None",
            font=("Helvetica", 12)
        )
        self.stocks_label.pack(pady=10)
        self.bind('<Return>', lambda event: self.plot_stock())
        
    def get_data_params(self):
        period = self.period_var.get()
        end = datetime.datetime.now()
        params = {
            "One Hour": {
                "start_date": self.one_hour_ago,
                "frequency": "5min",
                "resample": "5min"
            },
            "One Day": {
                "start_date": self.one_day_ago,
                "frequency": "30min",
                "resample": "30min"
            },
            "One Month": {
                "start_date": self.one_month_ago,
                "frequency": "daily",
                "resample": "daily"
            },
            "Six Months": {
                "start_date": self.six_months_ago,
                "frequency": "daily",
                "resample": "daily"
            },
            "One Year": {
                "start_date": self.one_year_ago,
                "frequency": "daily",
                "resample": "daily"
            },
            "All Time": {
                "start_date": end - relativedelta(years=20),
                "frequency": "daily",
                "resample": "daily"
            }
        }
        
        return params.get(period, params["Six Months"])
        
    def plot_stock(self):
        ticker = self.ticker_input.get().upper()        
        if not ticker:
            messagebox.showerror("Error", "Please enter a ticker symbol")
            return
            
        if ticker in self.all_tickers:
            messagebox.showerror("Error", f"{ticker} is already plotted!")
            return
            
        try:
            style.use("fivethirtyeight")
            
            params = self.get_data_params()
            end = datetime.datetime.now()
            
            # Get stock data
            stock_data = self.client.get_dataframe(
                ticker,
                frequency=params["frequency"],
                startDate=params["start_date"],
                endDate=end
            )
            
            if stock_data.empty:
                messagebox.showerror("Error", f"No data available for {ticker} in selected time period")
                return
                
            self.all_tickers.append(ticker)
            self.tickers_string = ", ".join(self.all_tickers)
            self.stocks_label.configure(text=f"Currently plotted stocks: {self.tickers_string}")
            
            stock_data["close"].plot(label=ticker)
            plt.title(f"{self.tickers_string} Stock Performance Over {self.period_var.get()}")
            plt.legend()
            
            plt.draw()
            plt.show(block=False)
            self.ticker_input.delete(0, 'end')            
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting {ticker}: {str(e)}")
            
    def clear_chart(self):
        if plt.get_fignums(): 
            plt.close('all')
        self.all_tickers = []
        self.tickers_string = ""
        self.stocks_label.configure(text="Currently plotted stocks: None")
        
if __name__ == "__main__":
    app = StockTrackerApp()
    app.mainloop()
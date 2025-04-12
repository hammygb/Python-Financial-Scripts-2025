# Python Script Name: HSBA.L_yahooquery_stockHistory_tkinter.py
# PyScripter IDE Version: 5.0.1.0 x 64
# Python Version: 3.11.8

import pandas as pd
import warnings
import tkinter as tk
from tkinter import ttk
from yahooquery import Ticker

# Suppress FutureWarnings and SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# Function to fetch historical data
def fetch_historical_data(ticker_symbol, start_date, end_date, output_file):
    # Fetch stock data
    stock = Ticker(ticker_symbol)
    hist_data = stock.history(start=start_date, end=end_date)

    if hist_data.empty:
        print(f"No data found for {ticker_symbol}.")
        return

    # Reset index to move 'date' from index to a column
    hist_data = hist_data.reset_index()

    # Keep only relevant columns and rename them
    hist_data = hist_data[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
    hist_data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Convert Date column to proper format
    hist_data['Date'] = pd.to_datetime(hist_data['Date']).dt.strftime('%Y-%m-%d')

    # Format Volume column with commas
    hist_data['Volume'] = hist_data['Volume'].apply(lambda x: f'{int(x):,}')

    # Sort by date
    hist_data = hist_data.sort_values(by='Date')

    # Save to CSV file
    hist_data.to_csv(output_file, index=False)
    print(f"Data for {ticker_symbol} saved to {output_file}")

    # Display the contents of the CSV file
    display_csv_data(output_file)

# Function to display CSV data in a Tkinter window
def display_csv_data(output_file):
    # Create a Tkinter window
    window = tk.Tk()
    window.title("HSBA.L Stock Data")

    # Get screen width and height to position the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set window size and position
    window.geometry(f"1030x300+{int((screen_width - 1920) / 2)}+{int((screen_height - 200) / 2)}")

    # Read the CSV file
    df = pd.read_csv(output_file)

    # Create a frame for the treeview (table) and scrollbar
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a treeview (table) widget
    tree = ttk.Treeview(frame, columns=df.columns.tolist(), show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Define column headings with bold font
    for col in df.columns:
        tree.heading(col, text=col, anchor=tk.W)
        tree.column(col, anchor=tk.W, width=140)  # Adjust the column width if needed

    # Insert the data rows into the treeview
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Apply normal font to data rows
    tree.tag_configure('normal', font=('Times New Roman', 11))

    # Create a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    tree.configure(yscrollcommand=scrollbar.set)

    # Apply style for alternating row colors
    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    fieldbackground="white",
                    font=('Times New Roman', 11),
                    borderwidth=1,  # This applies a small border for the entire treeview
                    relief="solid")
    style.configure("Treeview.Heading",
                    font=('Times New Roman', 12, 'bold'),
                    background="lightgray")
    style.map("Treeview",
              background=[('selected', 'lightblue')])

    # Customizing the Scrollbar
    style.configure("TScrollbar",
                    gripcount=0,
                    background="gray",  # Thumb color (the draggable part)
                    darkcolor="gray",    # Darker color for thumb's borders
                    lightcolor="gray")   # Lighter color for thumb's borders

    # Make the frame expand to fill the window
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Start the Tkinter event loop
    window.mainloop()

# Historical Stock Data
fetch_historical_data('HSBA.L',  # Stock Ticker symbol
                      '2025-03-04',  # Start Date
                      '2025-04-12',  # End Date
                      'HSBA.L_yahooquery_stockHistory.csv')  # CSV will be generated to save historical stock data

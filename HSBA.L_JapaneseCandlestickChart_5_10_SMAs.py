# Python Script Name: HSBA.L_JapaneseCandlestickChart_5_10_SMAs.py
# PyScripter Version: 5.0.1.0 x 64
# Python Version: 3.11.8

import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk
from tkinter import Frame
import os

# Function to add ordinal suffix to day
def add_ordinal_suffix(day):
    suffix = ["th", "st", "nd", "rd"] + ["th"] * 6  # handle 11-13 specially
    return f"{day}{suffix[day % 10] if day % 100 not in [11, 12, 13] else 'th'}"

# Function to validate the data for missing values
def validate_data(data):
    if data.isnull().sum().any():
        print("Warning: Missing values found in the dataset.")
        print(data.isnull().sum())  # Display missing values count

# Function to plot the candlestick chart with SMA
def plot_candlestick(data):
    # Extract OHLC data
    ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].dropna()

    # Convert 'Date' column to numerical format for candlestick plotting
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)

    # Check if we have valid data for plotting
    print(f"Data for plotting: {ohlc.head()}")

    if ohlc.empty:
        print("No valid OHLC data available.")
        return None  # Return None if no data to plot

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_ylim(650, 1000)  # Set the y-axis range manually
    fig.patch.set_facecolor('#ACE1AF')  # Outer background - Celadon Color

    # Plot the candlestick chart with custom colors and increased opacity
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='#00FF00', colordown='#FF0000', alpha=1.0)

    # Plot the 5-day SMA with a black border
    ax.plot(data['Date'][data['5_SMA'].notnull()],
            data['5_SMA'][data['5_SMA'].notnull()],
            color='skyblue', linewidth=3, label='5 Day SMA', solid_capstyle='round', solid_joinstyle='round')

    # Plot the 10-day SMA with a black border
    ax.plot(data['Date'][data['10_SMA'].notnull()],
            data['10_SMA'][data['10_SMA'].notnull()],
            color='violet', linewidth=3, label='10 Day SMA', solid_capstyle='round', solid_joinstyle='round')

    # Add a black border around the 5-day SMA line
    line_5 = ax.lines[-2]  # Get the last line (5-SMA)
    line_5.set_path_effects([pe.withStroke(linewidth=7, foreground='black')])  # Correct path effect usage

    # Add a black border around the 10-day SMA line
    line_10 = ax.lines[-1]  # Get the last line (10-SMA)
    line_10.set_path_effects([pe.withStroke(linewidth=7, foreground='black')])  # Correct path effect usage

    # Set the grid to be below the candlestick chart
    ax.set_axisbelow(True)

    # Customize the grid with bold lines
    ax.grid(True, color='black', linestyle='-', linewidth=0.9, alpha=0.8)

    # Manually add black borders around the candlesticks
    for idx, row in ohlc.iterrows():
        if row['Close'] >= row['Open']:
            lower = row['Open']
            upper = row['Close']
        else:
            lower = row['Close']
            upper = row['Open']

        rect = patches.Rectangle((row['Date'] - 0.3, lower), 0.6, upper - lower,
                                 edgecolor='black', facecolor='none', lw=1)
        ax.add_patch(rect)

    # Set labels and title with enhanced formatting
    ax.set_xlabel('5 - 10 Day SMAs & Stock Price Timeline', fontsize=12, fontweight='bold', labelpad=20,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    ax.set_ylabel('Price of Stock (GBP)', fontsize=12, fontweight='bold', labelpad=20,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    # Center the x-axis and y-axis labels manually
    ax.xaxis.set_label_coords(0.48, -0.10)   # '10 - 5 Day SMAs & Stock Price Timeline' label
    ax.yaxis.set_label_coords(-0.022, 0.50)  # 'Price of Stock (GBP)' label

    # Format start and end dates for the title
    start_date = data['Date'].min()
    end_date = data['Date'].max()

    # Create formatted strings
    start_date_str = f"{add_ordinal_suffix(start_date.day)} {start_date.strftime('%B %Y')}"
    end_date_str = f"{add_ordinal_suffix(end_date.day)} {end_date.strftime('%B %Y')}"

    # Customize the title's position and spacing
    fig.suptitle(f'HSBC Holdings plc (HSBA.L) - {start_date_str} - {end_date_str}',
                 fontsize=16, fontweight='bold',
                 x=0.5,  # Horizontal alignment (centered)
                 y=0.956,  # Vertical alignment (closer to top)
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Adjust margins to reduce excess space
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)  # Increased bottom margin

    # Ensure to keep tight layout after adjusting
    fig.tight_layout()

    # Format the x-axis to show dates properly
    date_format = mpl_dates.DateFormatter('%d-%m-%y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    # Set the inner background color to an almost black (very dark grey color)
    ax.set_facecolor('#1C1C1C')

    # Customize tick parameters
    ax.tick_params(axis='x', rotation=45, labelsize=10, width=1.5)  # Thicker ticks
    ax.tick_params(axis='y', labelsize=10, width=1.5)  # Thicker ticks for y-axis

    # Make dates bold
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')

    # Make y-axis tick labels bold
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')

    # Add a black border around the plot area
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)

    # Add a legend for the SMA lines with bold text
    legend = ax.legend(loc='upper left', fontsize=10, frameon=True, facecolor='white', edgecolor='black',
    framealpha=0.9) # Opaque background of legend label

    # Make the legend text bold
    for text in legend.get_texts():
        text.set_fontweight('bold')

    return fig  # Return the figure object for embedding in Tkinter

# Load the CSV file with proper date parsing and handle errors
try:
    data = pd.read_csv('HSBA.L_yahooquery_stockHistory.csv', parse_dates=['Date'], dayfirst=True)
except FileNotFoundError:
    print("Error: The file was not found.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Print the entire DataFrame
print("CSV data loaded successfully:\n")
print(data.head())  # Display the first few rows to check data

# Ensure 'Date' column is parsed correctly
data['Date'] = pd.to_datetime(data['Date'])

# Calculate the 10-day SMA
data['10_SMA'] = data['Close'].rolling(window=10).mean()  # 10-day SMA

# Calculate the 5-day SMA
data['5_SMA'] = data['Close'].rolling(window=5).mean()  # 5-day SMA

# Validate data
validate_data(data)

# Check if there are any NaNs in the '10_SMA' or '5_SMA' columns after calculating
if data['10_SMA'].isna().all() and data['5_SMA'].isna().all():
    print("No valid SMA data available.")

# Create the Tkinter application
root = tk.Tk()
root.title("5 - 10 Day SMAs - COA.L Japanese Candlestick Chart")

# Create a frame for the toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(side='bottom', fill='x')

# Create the figure and plot the candlestick chart
fig = plot_candlestick(data)

if fig:
    # Embed the figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # Create the navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    # Place the canvas and toolbar
    canvas.get_tk_widget().pack(fill='both', expand=True)
    toolbar_frame.pack(side='bottom', fill='x')

# Maximise window when script is run
root.state('zoomed')

# Start the Tkinter main loop
root.mainloop()

import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
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

# Function to plot the Fibonacci retracement levels with percentages and add a customized grouped legend
def plot_fibonacci_retracement(ax, data):
    high_price = data['High'].max()
    low_price = data['Low'].min()

    # Fibonacci levels: 0%, 23.6%, 38.2%, 50%, 61.8%, 100%
    fibonacci_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 1.0]
    colors = ['violet'] * len(fibonacci_levels)

    for level, color in zip(fibonacci_levels, colors):
        fib_price = low_price + (high_price - low_price) * level
        percentage = (fib_price - low_price) / (high_price - low_price) * 100  # Calculate the percentage

        # Draw Fibonacci line with black border
        line = ax.axhline(fib_price, color=color, linestyle='-', linewidth=3.0)
        line.set_path_effects([path_effects.Stroke(linewidth=5.0, foreground='black'),
                               path_effects.Normal()])

        # Place labels outside the grid on the right with bold text and white background
        ax.text(
            data['Date'].max() + pd.Timedelta(days=5),  # Increased offset for visibility
            fib_price,
            f'{fib_price:.2f} ({percentage:.2f}%)',  # Display the price level with percentage
            color='black',
            fontsize=10,
            fontweight='bold',
            verticalalignment='center',
            horizontalalignment='left',
            bbox=dict(facecolor='skyblue', edgecolor='black', linewidth=1.5, boxstyle='round,pad=0.5')
        )

    # Add grouped legend text directly below the x-axis, customize its position
    left_legend_text = [
        '100%: The highest price level of the stock',
        '61.8%: The price level that\'s 61.8% of the way',
        '50%: Halfway between the highest and lowest stock price (this is not a Fibonacci number but is commonly used)'
    ]
    right_legend_text = [
        '38.2%: The price level that\'s 38.2% of the way',
        '23.6%: The price level that\'s 23.6% of the way between the low and high',
        '0%: The lowest price level of the stock'
    ]

    # Position the left legend to the left of the center (customizable)
    left_legend_x = 0.25  # Adjust this to move the left legend
    for i, text in enumerate(left_legend_text):
        ax.text(
            left_legend_x,  # Position on the left side of the chart
            -0.10 - i * 0.05,  # Adjust vertical position to move it further down
            text,
            ha='center',
            va='top',
            fontsize=10,
            color='black',
            fontweight='bold',  # Make the text bold
            wrap=True,
            transform=ax.transAxes,  # Ensure the legend is positioned relative to the axis
            bbox=dict(facecolor='skyblue', edgecolor='black', linewidth=1.5, boxstyle='round,pad=0.5')
        )

    # Position the right legend to the right of the center (customizable)
    right_legend_x = 0.75  # Adjust this to move the right legend
    for i, text in enumerate(right_legend_text):
        ax.text(
            right_legend_x,  # Position on the right side of the chart
            -0.10 - i * 0.05,  # Adjust vertical position to move it further down
            text,
            ha='center',
            va='top',
            fontsize=10,
            color='black',
            fontweight='bold',  # Make the text bold
            wrap=True,
            transform=ax.transAxes,  # Ensure the legend is positioned relative to the axis
            bbox=dict(facecolor='skyblue', edgecolor='black', linewidth=1.5, boxstyle='round,pad=0.5')
        )

# Function to plot the candlestick chart
def plot_candlestick(data):
    # Extract OHLC data
    ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].dropna()

    # Convert 'Date' column to numerical format for candlestick plotting
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_ylim(650, 950)  # Set the y-axis range manually
    fig.patch.set_facecolor('#ACE1AF')  # Outer background - Celadon Color

    # Plot the candlestick chart with custom colors and increased opacity
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='#00FF00', colordown='#FF0000', alpha=1.0)

    # Set the grid to be below the candlestick chart
    ax.set_axisbelow(True)

    # Customize the grid with bold lines
    ax.grid(True, color='black', linestyle='-', linewidth=0.9, alpha=0.8)

    # Manually add black borders around the candlesticks
    for idx, row in ohlc.iterrows():
        if row['Close'] >= row['Open']:
            color = '#00FF00'  # fluorescent green
            lower = row['Open']
            upper = row['Close']
        else:
            color = '#FF0000'  # fluorescent red
            lower = row['Close']
            upper = row['Open']

        rect = patches.Rectangle((row['Date'] - 0.3, lower), 0.6, upper - lower,
                                 edgecolor='black', facecolor='none', lw=1)
        ax.add_patch(rect)

    # Set labels and title with enhanced formatting
    ax.set_xlabel('Fibonacci Resistance and Support Levels of Stock', fontsize=12, fontweight='bold', labelpad=20,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    ax.set_ylabel('Price of Stock (GBP)', fontsize=12, fontweight='bold', labelpad=20,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    # Center the x-axis and y-axis labels manually
    ax.xaxis.set_label_coords(0.48, -0.10)   # 'Fibonacci Resistance and Support Levels of Stock' label
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

    # Adjust the x-axis limits to move the candlesticks closer to the right
    ax.set_xlim(data['Date'].min() - pd.Timedelta(days=5), data['Date'].max() + pd.Timedelta(days=10))

    # Plot Fibonacci retracement levels once (only after xlim is set)
    plot_fibonacci_retracement(ax, data)

    # Force plot to be drawn and displayed
    plt.draw()
    return fig

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
print(data)  # Display the entire DataFrame

# Ensure 'Date' column is parsed correctly
print("\nDate column after parsing:\n")
print(data['Date'])  # Display the entire 'Date' column

# Convert 'Date' column to datetime if it’s not already
data['Date'] = pd.to_datetime(data['Date'])

# Check for duplicate dates
if data['Date'].duplicated().any():
    print("Warning: Duplicate dates found in data.")

# Validate data
validate_data(data)

# Create the Tkinter application
root = tk.Tk()
root.title("Fibonacci Retracement - HSBA.L Japanese Candlestick Chart")

# Create a frame for the toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Plot the candlestick chart
fig = plot_candlestick(data)

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# Add the NavigationToolbar2Tk to the window
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

# Position the canvas below the toolbar
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Maximise window when script is run
root.state('zoomed')

# Run the Tkinter event loop
root.mainloop()

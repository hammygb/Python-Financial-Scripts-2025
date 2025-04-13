import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.patches as patches
import matplotlib.lines as mlines
import matplotlib.patheffects as path_effects
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk
import os

# Load the CSV file
file_path = 'HSBA.L_dividends_2024_Present.csv'
df = pd.read_csv(file_path)

# Check the columns and preview the data
print("Columns in the CSV file:", df.columns)
print("Preview of data:", df.head())

# Ensure the 'Ex-dividend Date' column exists and is properly formatted
if 'Ex-dividend Date' not in df.columns:
    print("Error: 'Ex-dividend Date' column not found in CSV.")
else:
    df['Ex-dividend Date'] = pd.to_datetime(df['Ex-dividend Date'], utc=True)

# Check if 'Declared Dividend Amount (USD)' column exists and contains numeric values
if 'Declared Dividend Amount (USD)' not in df.columns:
    print("Error: 'Declared Dividend Amount (USD)' column not found in CSV.")
else:
    df['Declared Dividend Amount (USD)'] = pd.to_numeric(df['Declared Dividend Amount (USD)'], errors='coerce')  # Convert 'Dividend' to numeric

# Adjust ex-dividend dates to Thursdays for UK stocks
if '.L' in file_path:
    df['Ex-dividend Date'] = df['Ex-dividend Date'].apply(lambda date: date + pd.DateOffset(days=(3 - date.weekday()))
                                                         if date.weekday() != 3 else date)

# Filter data from 2024 to present
df_filtered = df[df['Ex-dividend Date'] >= '2024-01-01']
df_filtered = df_filtered.sort_values('Ex-dividend Date')

# Separate data for each year
dividend_data_by_year = {
    2024: df_filtered[df_filtered['Ex-dividend Date'].dt.year == 2024],
    2025: df_filtered[df_filtered['Ex-dividend Date'].dt.year == 2025],
}

# Create a Tkinter window
root = tk.Tk()
root.title("HSBA.L Dividend Bar Chart")

# Create the figure with a Celadon outer background
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#ACE1AF')
ax.set_ylim(0.0, 0.40)  # Set the y-axis range manually

# Define x-axis positions for each year with spacing
start_pos = 0
x_positions = {}
for year, data in dividend_data_by_year.items():
    x_positions[year] = range(start_pos, start_pos + len(data))
    start_pos += len(data) + 2  # Add spacing between years

# Define colors for each year
colors = {
    2024: 'royalblue', 2025: 'sandybrown'
}

# Plotting bars for each year
for year, data in dividend_data_by_year.items():
    ax.bar(
        x_positions[year],
        data['Declared Dividend Amount (USD)'],
        color=colors[year],
        edgecolor='black',
        linewidth=2,
        zorder=2,
        label=f'Year {year} Dividends'
    )

# Create the legend without a title, with bold text
legend = ax.legend(
    loc='upper left',
    fontsize=11,
    frameon=True,
    fancybox=True,
    framealpha=0.9,  # Opaque background of legend label
    borderpad=1,
    edgecolor='black',  # Thin black border around the legend
    borderaxespad=1,    # Padding between legend border and label
    prop={'weight': 'bold'}  # Make legend text bold
)

# Set title and axis labels
ax.set_title('HSBA.L Dividend History (2024 to Present)', fontsize=14, fontweight='bold',
             x=0.5, y=1.025,
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

ax.set_ylabel('Declared Dividend Amounts (USD)', fontsize=12, fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

ax.set_xlabel('Ex-Dividend Dates (United Kingdom)', fontsize=12, fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

# Center x and y-axis label coordinates
ax.xaxis.set_label_coords(0.50, -0.045) # 'Thursday Ex-Dividend Dates (United Kingdom)' label
ax.yaxis.set_label_coords(-0.028, 0.50) # 'Dividend Amounts' label

# Set dark grey background color
ax.set_facecolor('#1C1C1C')

# Add grid behind the bars
ax.grid(visible=True, which='both', axis='y', color='black', linestyle='-', linewidth=1, zorder=1)

# Set a black border around the grid box
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(1.5)

# Make y-axis numbers bold
for label in ax.get_yticklabels():
    label.set_fontweight('bold')
    label.set_fontsize(11)

# Set x-axis labels to dates with bold font
xticks = []
xtick_labels = []
for year, data in dividend_data_by_year.items():
    xticks.extend(x_positions[year])
    xtick_labels.extend(data['Ex-dividend Date'].dt.strftime('%d-%m-%Y').tolist())

# Set x-axis labels to dates with smaller font for 2-year dividend timeline
ax.set_xticks(xticks)
ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')  # Increased font size to 12

# Display the chart on Tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add toolbar at the bottom
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Maximize window
root.state('zoomed')

# Start Tkinter main loop
plt.tight_layout()
canvas.draw()
root.mainloop()

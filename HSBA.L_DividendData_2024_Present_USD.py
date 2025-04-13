# Python Script Name: HSBA.L_DividendData_2024_Present_USD.py
# PyScripter IDE Version: 5.0.1.0 x 64
# Python Version: 3.11.8

import csv
import os

# Define the headers
headers = ['Ex-dividend Date', 'Declared Dividend Amount (USD)']

# Define the filename
filename = 'HSBA.L_dividends_2024_Present.csv'

# Check if the CSV file already exists
file_exists = os.path.isfile(filename)

# Open the CSV file in append mode, creating it if necessary
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)

    # If the file does not exist, write the header
    if not file_exists:
        writer.writerow(headers)
        print(f"CSV file '{filename}' created with headers.")

    # Let the user add dividend entries
    while True:
        # Get user input for Ex-dividend Date and Declared Dividend Amount
        ex_dividend_date = input("Enter the Ex-dividend Date (MM/DD/YYYY) or type 'exit' to stop: ")

        if ex_dividend_date.lower() == 'exit':
            print("Exiting the program...")
            break

        declared_dividend_amount = input("Enter the Declared Dividend Amount (USD): ")

        # Add validation (you can add more here as needed)
        try:
            # Attempt to convert the dividend amount to a float
            declared_dividend_amount = float(declared_dividend_amount)
        except ValueError:
            print("Invalid amount. Please enter a valid numeric value.")
            continue

        # Write the new entry to the CSV file
        writer.writerow([ex_dividend_date, declared_dividend_amount])
        print(f"Entry added: {ex_dividend_date}, {declared_dividend_amount} GBP")

print(f"Data has been added to '{filename}' successfully!")

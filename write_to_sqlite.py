import os
import pandas as pd
import sqlite3
from openpyxl import load_workbook

# Tutorial Code: List the available methods of the SQLite database
def tutorial_code():
    print("Here is a basic tutorial for SQLite operations:")
    print("\n1. Create a connection to a SQLite database:")
    print("   conn = sqlite3.connect('your_database.db')")
    print("\n2. Create a table:")
    print("   conn.execute('''CREATE TABLE IF NOT EXISTS your_table (column1 TEXT, column2 INTEGER)''')")
    print("\n3. Insert data into the table:")
    print("   conn.execute('''INSERT INTO your_table (column1, column2) VALUES (?, ?)''', (value1, value2))")
    print("\n4. Fetch data from the table:")
    print("   cursor = conn.execute('''SELECT * FROM your_table''')")
    print("   for row in cursor:")
    print("       print(row)")

# Function to get Excel files from a directory
def get_excel_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.xls') or f.endswith('.xlsx')]

# Function to read Excel file and convert it into a DataFrame
def read_excel_to_df(excel_file_path):
    try:
        wb = load_workbook(excel_file_path)
        sheet = wb.active
        data = sheet.values
        cols = next(data)
        df = pd.DataFrame(data, columns=cols)
        return df
    except Exception as e:
        print(f"Error reading {excel_file_path}: {e}")
        return None

# Function to display the first few rows of the DataFrame (for previewing)
def preview_data(df):
    print("Here is a preview of the data:")
    print(df.head())  # Show the first 5 rows of the DataFrame

# Function to write DataFrame to SQLite database
def write_to_sqlite(df, db_name):
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql('data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data written to database {db_name}.")
    except Exception as e:
        print(f"Error writing to database {db_name}: {e}")

def main():
    # Print tutorial code
    tutorial_code()

    # Ask user for the directory containing Excel files
    input_directory = input("Enter the path to the directory containing Excel files: ")

    # Check if the directory exists
    if not os.path.isdir(input_directory):
        print(f"The directory '{input_directory}' does not exist!")
        return

    # Get the list of Excel files in the directory
    excel_files = get_excel_files(input_directory)

    # Check if there are any Excel files
    if not excel_files:
        print(f"No Excel files found in {input_directory}.")
        return

    print(f"Found Excel files: {excel_files}")

    # Process each Excel file
    for excel_file in excel_files:
        excel_file_path = os.path.join(input_directory, excel_file)
        print(f"Processing {excel_file_path}...")

        # Read the Excel file into a DataFrame
        df = read_excel_to_df(excel_file_path)
        if df is not None:
            # Preview the data before saving it
            preview_data(df)

            # Ask user if they want to continue with saving this data
            save_data = input(f"Do you want to save the data from {excel_file} to the database? (y/n): ").strip().lower()

            if save_data == 'y':
                # Create a database name based on the Excel file name
                db_name = f"output_{os.path.splitext(excel_file)[0]}.db"
                
                # Write DataFrame to SQLite database
                write_to_sqlite(df, db_name)
            else:
                print(f"Skipping {excel_file}.")

if __name__ == "__main__":
    main()
# This script provides a basic tutorial for SQLite operations and allows the user to read Excel files from a specified directory,
# preview the data, and save it to a SQLite database. It includes error handling for file reading and database writing operations.
# The script also checks if the specified directory exists and if there are any Excel files to process.


import pandas as pd
import os
import glob
import argparse
import sqlite3
from datetime import datetime

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process Excel files and export to CSV and SQLite.")
    parser.add_argument("input_directory", help="Directory containing Excel files")
    args = parser.parse_args()

    # Find all Excel files in the directory
    excel_files = glob.glob(os.path.join(args.input_directory, "*.xlsx"))
    if not excel_files:
        print("No Excel files found in the specified directory.")
        return

    # Read and combine all Excel files into a single DataFrame
    all_data = []
    for file in excel_files:
        try:
            xls = pd.ExcelFile(file)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df['SourceFile'] = os.path.basename(file)
                df['SheetName'] = sheet_name
                all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not all_data:
        print("No data could be read from the Excel files.")
        return

    # Concatenate and clean DataFrame
    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.dropna(how='all')  # Drop rows where all columns are NaN

    # Create output filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"output_{timestamp}.csv"
    output_db = f"output_{timestamp}.db"

    # Save to CSV
    final_df.to_csv(output_csv, index=False)
    print(f"Data written to CSV file: {output_csv}")

    # Save to SQLite database using pandas to_sql
    conn = sqlite3.connect(output_db)
    final_df.to_sql("combined_data", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data written to SQLite database: {output_db}")

if __name__ == "__main__":
    main()

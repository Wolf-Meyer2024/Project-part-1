import os
import sys
import pandas as pd
from pathlib import Path

try:
    import openpyxl  # Ensure openpyxl is installed
except ImportError:
    print("Error: The 'openpyxl' module is required but not installed. Install it using 'pip install openpyxl'.")
    sys.exit(1)

def find_excel_files(directory):
    """Recursively find all .xlsx files in the given directory."""
    return list(Path(directory).rglob("*.xlsx"))

def read_excel_file(file_path):
    """Read all sheets of an Excel file into DataFrames."""
    try:
        all_sheets = pd.read_excel(file_path, sheet_name=None, dtype=str, engine='openpyxl')
        return [df for df in all_sheets.values() if df is not None]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def merge_dataframes(files):
    """Merge all DataFrames from all Excel files, maintaining all original columns."""
    all_data = []
    for file in files:
        dfs = read_excel_file(file)
        all_data.extend(dfs)

    if not all_data:
        return None

    merged_df = pd.concat(all_data, ignore_index=True)
    return merged_df

def process_dataframe(df):
    """Clean and sort the DataFrame."""
    # Attempt to convert Date and Time columns
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time

    # Sort if applicable
    sort_cols = [col for col in ['Date', 'Time'] if col in df.columns]
    if sort_cols:
        df = df.sort_values(by=sort_cols)

    # Round numerical columns
    for col in df.select_dtypes(include=['float', 'int']).columns:
        df[col] = df[col].round(1)

    return df

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process Excel files into a single CSV.")
    parser.add_argument("input_directory", help="Directory containing Excel files")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    if not os.path.isdir(args.input_directory):
        print("Error: The specified directory does not exist.")
        sys.exit(1)

    excel_files = find_excel_files(args.input_directory)
    if not excel_files:
        print("Error: No .xlsx files found in the specified directory.")
        sys.exit(1)

    merged_df = merge_dataframes(excel_files)
    if merged_df is None:
        print("Error: No valid data extracted from Excel files.")
        sys.exit(1)

    processed_df = process_dataframe(merged_df)

    # 🔍 Preview the data before exporting
    print("\n--- Data Preview ---")
    print(processed_df.head(10))

    try:
        processed_df.to_csv(args.output_file, index=False)
        print(f"Data successfully written to {args.output_file}")
    except Exception as e:
        print(f"Error writing to {args.output_file}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

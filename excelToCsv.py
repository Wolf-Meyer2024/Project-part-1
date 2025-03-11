import os
import sys
import pandas as pd
from pathlib import Path

try:
    import openpyxl  # Ensure openpyxl is installed
except ImportError:
    print("Error: The 'openpyxl' module is required but not installed. Install it using 'pip install openpyxl'.")
    sys.exit(1)

def create_sample_excel(directory):
    """Creates a sample Excel file for testing if no files exist."""
    os.makedirs(directory, exist_ok=True)
    sample_file = os.path.join(directory, "sample.xlsx")
    
    if not os.path.exists(sample_file):
        data = {
            "Date": ["2025-03-01", "2025-03-02"],
            "Time": ["12:30:00", "14:45:00"],
            "MachineID": [101, 102],
            "Value": [23.5, 45.8]
        }
        df = pd.DataFrame(data)
        df.to_excel(sample_file, index=False, engine='openpyxl')
        print(f"Sample Excel file created: {sample_file}")

def find_excel_files(directory):
    """Recursively find all .xlsx files in the given directory."""
    return list(Path(directory).rglob("*.xlsx"))

def read_excel_file(file_path):
    """Read an Excel file into a Pandas DataFrame, handling errors gracefully."""
    try:
        df = pd.read_excel(file_path, dtype=str, engine='openpyxl')  # Ensure openpyxl is used
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def merge_dataframes(files):
    """Merge all DataFrames while ensuring consistent column order."""
    all_data = []
    columns_order = None
    
    for file in files:
        df = read_excel_file(file)
        if df is not None:
            if columns_order is None:
                columns_order = df.columns.tolist()  # Establish column order from the first valid file
            else:
                df = df.reindex(columns=columns_order, fill_value="")  # Maintain column order
            all_data.append(df)
    
    if not all_data:
        return None, columns_order
    
    merged_df = pd.concat(all_data, ignore_index=True)
    return merged_df, columns_order

def process_dataframe(df):
    """Sort the DataFrame by Date, Time, and MachineID, and format values correctly."""
    if 'Date' in df.columns and 'Time' in df.columns and 'MachineID' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
        df['MachineID'] = pd.to_numeric(df['MachineID'], errors='coerce')
        df = df.sort_values(by=['Date', 'Time', 'MachineID'], ascending=[True, True, True])
    
    # Convert floats to one decimal place
    df = df.applymap(lambda x: f"{float(x):.1f}" if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)
    
    return df

def main(output_file="output.csv", input_directory="test_files"):
    if not os.path.isdir(input_directory):
        print("Warning: The specified directory does not exist. Creating test directory with sample data.")
        create_sample_excel(input_directory)
    
    excel_files = find_excel_files(input_directory)
    if not excel_files:
        print("Warning: No .xlsx files found. Creating a sample Excel file.")
        create_sample_excel(input_directory)
        excel_files = find_excel_files(input_directory)
    
    merged_df, columns_order = merge_dataframes(excel_files)
    if merged_df is None:
        print("Error: No valid data extracted from Excel files.")
        sys.exit(1)
    
    processed_df = process_dataframe(merged_df)
    
    # Write to CSV
    try:
        processed_df.to_csv(output_file, index=False)
        print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()

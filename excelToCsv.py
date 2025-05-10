import os
import glob
import pandas as pd
from datetime import datetime

def get_valid_output_filename():
    while True:
        filename = input("💾 Enter the desired name for the output CSV file (e.g. output.csv): ").strip()
        if not filename.endswith(".csv"):
            print("❌ Output filename must end with '.csv'. Please try again.")
        elif os.path.exists(filename):
            confirm = input(f"⚠️ File '{filename}' already exists. Overwrite? (y/n): ").strip().lower()
            if confirm == 'y':
                return filename
        else:
            return filename

def get_valid_directory():
    while True:
        input_path = input("📁 Enter the path to the directory containing Excel files: ").strip()

        if os.path.isfile(input_path):
            print("❌ You entered a file path, but this program needs a folder path.")
            print("💡 Tip: Remove the filename from the end and just enter the folder path.")
        elif not os.path.isdir(input_path):
            print(f"❌ The path '{input_path}' does not exist or is not a directory. Please try again.")
        else:
            return input_path

def find_excel_files(directory):
    excel_files = glob.glob(os.path.join(directory, "**", "*.xlsx"), recursive=True)
    if not excel_files:
        print("❌ No Excel (.xlsx) files found in the directory or its subdirectories.")
        return []
    return excel_files

def process_excel_files(excel_files):
    all_data = []
    for file in excel_files:
        try:
            xls = pd.ExcelFile(file)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
                df['SourceFile'] = os.path.basename(file)
                df['SheetName'] = sheet_name
                all_data.append(df)
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")
    return all_data

def clean_and_sort_data(dataframes):
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.dropna(how='all')

    # Round numeric columns to 1 decimal
    for col in combined_df.select_dtypes(include=['float']):
        combined_df[col] = combined_df[col].round(1)

    # Fill blanks with empty strings
    combined_df = combined_df.fillna("")

    # Sort if fields are available
    sort_fields = [col for col in ['Date', 'Time', 'MachineID'] if col in combined_df.columns]
    combined_df = combined_df.sort_values(by=sort_fields, ignore_index=True)

    return combined_df

def main():
    print("📊 Welcome to Excel ➜ CSV Converter")

    output_filename = get_valid_output_filename()
    input_directory = get_valid_directory()

    excel_files = find_excel_files(input_directory)
    if not excel_files:
        return

    dataframes = process_excel_files(excel_files)
    if not dataframes:
        print("❌ No valid data could be read from the Excel files.")
        return

    final_df = clean_and_sort_data(dataframes)

    try:
        final_df.to_csv(output_filename, index=False)
        print(f"✅ Data successfully written to '{output_filename}'")
    except Exception as e:
        print(f"❌ Failed to write CSV file: {e}")

if __name__ == "__main__":
    main()

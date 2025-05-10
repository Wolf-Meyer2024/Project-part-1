def main():
    import argparse
    import sqlite3

    parser = argparse.ArgumentParser(description="Process Excel files into a single output file (CSV or SQLite).")
    parser.add_argument("input_directory", help="Directory containing Excel files")
    parser.add_argument("output_file", help="Path to the output CSV or SQLite (.db) file")
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

    # Sort by Date, Time, MachineID if available
    sort_cols = [col for col in ['Date', 'Time', 'MachineID'] if col in processed_df.columns]
    if sort_cols:
        processed_df = processed_df.sort_values(by=sort_cols)

    print("\n--- Data Preview ---")
    print(processed_df.head(10))

    try:
        if args.output_file.lower().endswith('.csv'):
            processed_df.to_csv(args.output_file, index=False)
            print(f"Data successfully written to {args.output_file}")
        elif args.output_file.lower().endswith('.db'):
            conn = sqlite3.connect(args.output_file)
            processed_df.to_sql("sensor_data", conn, if_exists="replace", index=False)
            conn.close()
            print(f"Data successfully written to SQLite database: {args.output_file}")
        else:
            print("Error: Output file must end with .csv or .db")
            sys.exit(1)
    except Exception as e:
        print(f"Error writing output: {e}")
        sys.exit(1)

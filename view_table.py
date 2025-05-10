import sqlite3
import pandas as pd

# Function to read and display data from the SQLite table
def read_from_sqlite(db_name, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    
    # Use pandas to read data from the specified table
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()

    # Return the DataFrame (table data)
    return df

# Main code to execute
if __name__ == "__main__":
    # Define the database and table names
    db_name = 'test_database.db'
    table_name = 'TestTable'
    
    # Read and display the data
    data = read_from_sqlite(db_name, table_name)
    
    # Print the data as a table
    print("Data from the table:")
    print(data)

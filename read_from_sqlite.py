import sqlite3
import pandas as pd

# Replace this with the actual name of your .db file
db_filename = 'output_20250510_093459.db'  # Update if your filename is different
table_name = 'your_table_name'  # Replace this with the table name you used in to_sql()

# Connect to the database
conn = sqlite3.connect(db_filename)

# Read the data into a pandas DataFrame
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

# Display the DataFrame
print(df)

# Close the connection
conn.close()

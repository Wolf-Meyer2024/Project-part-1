import pandas as pd
import sqlite3
from datetime import datetime
import os

# Sample DataFrame for demonstration
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 92, 78]
}
df = pd.DataFrame(data)

# Step 1: Generate a database file name with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
db_filename = f"output_{timestamp}.db"

# Step 2: Create a connection to the SQLite database
conn = sqlite3.connect(db_filename)

# Step 3: Write the DataFrame to the database
# This will create a table named 'student_scores'
df.to_sql('student_scores', conn, if_exists='replace', index=False)

# Step 4: Close the connection
conn.close()

print(f"Data written to SQLite database: {db_filename}")

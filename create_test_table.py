import sqlite3

# Step 1: Create a database and connect
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Step 2: Create a test table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestTable (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INTEGER,
        Major TEXT
    )
''')

# Step 3: Insert some sample data
sample_data = [
    ('Alice', 21, 'Computer Science'),
    ('Bob', 22, 'Mathematics'),
    ('Charlie', 20, 'Biology')
]

cursor.executemany('''
    INSERT INTO TestTable (Name, Age, Major) VALUES (?, ?, ?)
''', sample_data)

# Step 4: Commit and close
conn.commit()
conn.close()

print("✅ Test table 'TestTable' created with sample data in 'test_database.db'")

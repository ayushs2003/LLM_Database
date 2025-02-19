import sqlite3

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect("records.db")
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    age INTEGER
)
''')

# Insert sample data
students_data = [
    ("Alice", "CS", 21),
    ("Bob", "IT", 22),
    ("Charlie", "CS", 23),
    ("David", "ECE", 20),
    ("Eve", "IT", 24)
]

cursor.executemany("INSERT INTO students (name, department, age) VALUES (?, ?, ?)", students_data)

# Save and close
conn.commit()
conn.close()

print("Database setup complete!")

import pandas as pd
import sqlite3

# Read Excel file
df = pd.read_excel('Dataset.xlsx')  # Replace with your file path

# Connect to SQLite database
conn = sqlite3.connect('courses.db')

# Import all data to SQLite table
df.to_sql('courses', conn, if_exists='replace', index=False)

# Close connection

conn.close()

print("All courses imported successfully!")




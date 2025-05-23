
import sqlite3
import pandas as pd
from datetime import datetime
import uuid

DB_PATH = "courses.db"
EXCEL_PATH = "Dataset.xlsx"

def init_db():
    conn = sqlite3.connect(DB_PATH)

    # Create table if not exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT,
            description TEXT,
            category TEXT,
            language TEXT,
            duration_hours REAL,
            price REAL,
            average_rating REAL,
            created_date TEXT,
            created_by TEXT,
            modified_date TEXT,
            modified_by TEXT,
            is_deleted TEXT,
            course_highlights TEXT,
            is_status REAL,
            course_faq TEXT,
            external_id TEXT,
            discount REAL
        )
    ''')
    conn.commit()

    # If table is empty, load existing Dataset.xlsx into DB
    cursor = conn.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        try:
            df = pd.read_excel("Dataset.xlsx")
            df.to_sql("courses", conn, if_exists="append", index=False)
            print("📥 Imported existing Dataset.xlsx into database.")
        except FileNotFoundError:
            print("⚠ No existing Dataset.xlsx found.")
    conn.close()



def add_course_to_db(course):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', course)
    conn.commit()
    conn.close()
    print("✅ Course added to database.")
    export_db_to_excel()

def export_db_to_excel():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM courses", conn)
    try:
        df.to_excel(EXCEL_PATH, index=False)
        print("📁 Excel file updated.")
    except PermissionError:
        print("❌ Failed to update Excel file. Please close it if it's open and try again.")
    finally:
        conn.close()

def main():
    init_db()

    print("Enter the following details to add a new course:")
    course_id = str(uuid.uuid4())
    course_name = input("Course Name: ")
    description = input("Description: ")
    category = input("Category: ")
    language = input("Language: ")
    duration_hours = float(input("Duration (hours): "))
    price = float(input("Price: "))
    average_rating = float(input("Average Rating (0-5): "))
    created_date = datetime.now().isoformat()
    created_by = str(uuid.uuid4())
    modified_date = created_date
    modified_by = created_by
    is_deleted = "0"
    course_highlights = "[{'feature': 'Certificate included'}]"
    is_status = 1.0
    course_faq = "[{'question': 'Do I get a certificate?', 'answer': 'Yes'}]"
    external_id = str(uuid.uuid4())
    discount = float(input("Discount (%): "))

    course = (
        course_id, course_name, description, category, language,
        duration_hours, price, average_rating, created_date, created_by,
        modified_date, modified_by, is_deleted, course_highlights,
        is_status, course_faq, external_id, discount
    )

    add_course_to_db(course)

if __name__ == "__main__":
    main()

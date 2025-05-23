# 📚 AI-Powered Course Recommendation System

This project is an AI-based course recommendation system built with Python, Streamlit, scikit-learn, and SQLite. It helps users discover relevant courses based on topics of interest, filtering options, and content similarity using TF-IDF and cosine similarity.

## 💡 How it Works

1.TF-IDF is used to vectorize course titles, descriptions, and categories.
2.Cosine similarity is calculated between user input and all course vectors.
3.Recommendations are filtered by similarity threshold and optionally by language.
4.Top results are shown to the user in a clean UI.

## 🚀 Features

- 🔍 Search and recommend similar courses by topic or course name.
- 🌐 Filter courses by language.
- ⭐ View top-rated courses.
- 🧠 NLP-based similarity matching using TF-IDF and cosine similarity.
- 🧾 Admin script to import Excel course data into SQLite.
- ➕ Script to add new courses into the database and update the Excel dataset.

---

 

## 📂 Project Structure

```bash
.
├── main_app.py              # Streamlit-based frontend for recommendations
├── excel_to_sql.py          # One-time script to import Excel data into SQLite
├── add_course.py            # Script to add a new course via CLI input
├── Dataset.xlsx             # Main dataset of courses (Excel format)
└── courses.db               # SQLite database storing all course data


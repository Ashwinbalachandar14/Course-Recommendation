import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load and process data
@st.cache_data(ttl=60)
def load_data(filepath):
    df = pd.read_excel("Dataset.xlsx")

    # Drop duplicate course names
    df.drop_duplicates(subset='course_name', inplace=True)

    # Drop rows with missing values in critical columns
    df.dropna(subset=['course_name', 'description', 'category', 'language', 'duration_hours'], inplace=True)

    # Prepare text for TF-IDF
    df['text'] = df['course_name'].astype(str) + ' ' + df['description'].astype(str) + ' ' + df['category'].astype(str)

    return df


def get_tfidf_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['text'])
    return tfidf_matrix, tfidf


def get_recommendations_for_topic(topic, df, tfidf_vectorizer, threshold=0.2, language_filter=None):
    course_inputs = [t.strip() for t in topic.split(",") if t.strip()]
    all_results = pd.DataFrame()

    # Apply language filter before similarity
    if language_filter and language_filter.lower() != "all":
        df = df[df['language'].str.lower() == language_filter.lower()]

    if df.empty:
        return pd.DataFrame()  # No course matches the filters

    # Compute TF-IDF matrix on filtered df
    tfidf_matrix = tfidf_vectorizer.transform(df['text'])

    for course in course_inputs:
        topic_vector = tfidf_vectorizer.transform([course])
        sim_scores = cosine_similarity(topic_vector, tfidf_matrix).flatten()

        df_copy = df.copy()
        df_copy['similarity'] = sim_scores

        # Exclude the exact same course name if present
        df_copy = df_copy[~df_copy['course_name'].str.lower().eq(course.lower())]

        filtered = df_copy[df_copy['similarity'] > threshold]

        if len(course_inputs) == 1:
            # Single input: return top 5 if >=5 results; else return all that passed the threshold
            if len(filtered) >= 5:
                top_matches = filtered.sort_values(by='similarity', ascending=False).head(5)
            else:
                top_matches = filtered.sort_values(by='similarity', ascending=False)
        else:
            # Multiple inputs: always return top 2 for each input (if available)
            top_matches = filtered.sort_values(by='similarity', ascending=False).head(2)

        all_results = pd.concat([all_results, top_matches])

    all_results = all_results.drop_duplicates(subset='course_name')
    return all_results.sort_values(by='similarity', ascending=False)[
        ['course_id', 'course_name', 'language', 'duration_hours']]



# Streamlit UI
def main():
    st.set_page_config(page_title="Course Recommendation System", layout="wide")
    st.title("📚 AI-Powered Course Recommendation System")

    # Load data
    df = load_data("Dataset.xlsx")
    tfidf_matrix, tfidf_vectorizer = get_tfidf_matrix(df)

    # Sidebar filters
    st.sidebar.header("🔎 Filters")
    selected_language = st.sidebar.selectbox("Select Language",
                                             options=["All"] + sorted(df['language'].dropna().unique().tolist()))
    # max_duration slider removed

    # Set a fixed threshold
    threshold = 0.25  # static value

    # Top rated
    st.subheader("🔥 Top 7 Highest Rated Courses")
    if 'average_rating' in df.columns:
        top_rated = df.sort_values(by='average_rating', ascending=False).head(7)
        for idx, row in top_rated.iterrows():
            st.markdown(f"✅ {row['course_name']} — ⭐ {row['average_rating']} ({row['language']}, {row['duration_hours']} hrs)")
    else:
        st.warning("⚠ 'average_rating' column not found.")

    # Search
    st.subheader("🎯 Find Recommended Courses")
    user_input = st.text_input("Type the course name or topic (e.g., Data Science, AI, Cloud):")

    # Check if user_input has any non-whitespace characters
    if user_input and user_input.strip():
        recommendations = get_recommendations_for_topic(
            user_input, df, tfidf_vectorizer,
            threshold=threshold,
            language_filter=selected_language
        )
        if not recommendations.empty:
            st.success(f"Showing results for: {user_input}")
            st.dataframe(recommendations.reset_index(drop=True))
        else:
            st.info("⚠ No similar courses found for your input and filters.")
    # If input is empty or just whitespace, do nothing (no recommendation or message)


if __name__ == "__main__":
    main()


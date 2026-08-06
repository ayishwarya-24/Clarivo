import streamlit as st
import plotly.express as px
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import re

def extract_phrases(text):

    phrases = []

    patterns = [
        r"battery life",
        r"sound quality",
        r"customer service",
        r"delivery experience",
        r"bluetooth disconnects",
        r"app crashes",
        r"stopped working",
        r"value for money"
    ]

    text = text.lower()

    for pattern in patterns:
        if pattern in text:
            phrases.append(pattern.title())

    return phrases

stop_words = {"the","and","for","with","after","very","this","that","from",
    "have","has","had","was","were","are","is","a","an","of","to","in"}

st.set_page_config(
    page_title="Clarivo",
    layout="wide"
)

# -----------------------------
# SAMPLE DATA
# -----------------------------



# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:
    st.title("Clarivo")

    st.markdown("---")

    st.write("Dashboard")
    st.write("Review Analysis")
    st.write("Insights")
    st.write("AI Assistant")



total_reviews = 0
positive_reviews = 0
negative_reviews = 0
neutral_reviews = 0

sentiment_data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Count": [0, 0, 0]
})

bar_data = pd.DataFrame({
    "Category": ["Positive", "Negative", "Neutral"],
    "Count": [0, 0, 0]
})

has_data = False

if not has_data:

    st.title("Clarivo")

    st.subheader(
        "AI-Powered Customer Feedback Intelligence Platform"
    )

    st.write(
        """
        Transform customer reviews into actionable insights using
        sentiment analysis and intelligent feedback analysis.
        """
    )

    st.markdown("---")

    st.markdown("### How It Works")

    st.markdown("""
    1. Upload a CSV containing customer reviews
    2. Analyze customer sentiment automatically
    3. Discover common praises and complaints
    4. Generate AI-powered insights
    """)

    st.markdown("---")

    st.markdown("### Features")

    st.success("Sentiment Analysis")
    st.success("AI Insights")
    st.success("Complaint Detection")
    st.success("Interactive Analytics Dashboard")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Reviews CSV",
        type=["csv"]
    )

    st.caption(
        "CSV must contain a column named 'Review'."
    )

    if uploaded_file is not None:
        has_data = True



if has_data:

    st.title("Clarivo Dashboard")

    st.caption(
        "Monitor customer sentiment and discover actionable insights."
    )

    reviews_df = pd.read_csv(uploaded_file)
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for review in reviews_df["Review"]:
        score = analyzer.polarity_scores(str(review))
        compound = score["compound"]

        if compound >= 0.05:
            sentiments.append("Positive")

        elif compound <= -0.05:
            sentiments.append("Negative")

        else:
            sentiments.append("Neutral")

    reviews_df["Sentiment"] = sentiments

    positive_phrases = []
    negative_phrases = []
    
    for review in reviews_df[
        reviews_df["Sentiment"] == "Positive"
        ]["Review"]:
        
        positive_phrases.extend(
            extract_phrases(str(review))
        )

    for review in reviews_df[
        reviews_df["Sentiment"] == "Negative"
        ]["Review"]:
        
        negative_phrases.extend(
            extract_phrases(str(review))
        )
    
    top_praises = Counter(positive_phrases).most_common(5)
    
    top_complaints = Counter(negative_phrases).most_common(5)
    
    total_reviews = len(reviews_df)

    positive_reviews = len(reviews_df[reviews_df["Sentiment"] == "Positive"])
    
    negative_reviews = len(reviews_df[reviews_df["Sentiment"] == "Negative"])
    
    neutral_reviews = len(reviews_df[reviews_df["Sentiment"] == "Neutral"])

    overall_sentiment = "Positive"
    if negative_reviews > positive_reviews:
        overall_sentiment = "Negative"
        
    elif neutral_reviews > positive_reviews:
        overall_sentiment = "Neutral"

    positive_topics = []
    
    for word, count in top_praises[:3]:
        if len(word) > 3:
            positive_topics.append(word)
            
    negative_topics = []
    
    for word, count in top_complaints[:3]:
        if len(word) > 3:
            negative_topics.append(word)
    
    ai_summary = f"""
    Overall customer sentiment is {overall_sentiment.lower()}.
    Most praised topics include:
    {", ".join(positive_topics)}.
    Most common complaints include:
    {", ".join(negative_topics)}.
    """

    sentiment_data = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [
            positive_reviews,
            negative_reviews,
            neutral_reviews
        ]
    })

    bar_data = pd.DataFrame({
        "Category": ["Positive", "Negative", "Neutral"],
        "Count": [
            positive_reviews,
            negative_reviews,
            neutral_reviews
        ]
    })

    st.success("Analysis completed")

    st.subheader("Analyzed Reviews")

    st.dataframe( reviews_df, width="stretch" )

if has_data:
    st.markdown("---")

if has_data:

# -----------------------------
# KPI CARDS
# -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Reviews", total_reviews)

    with col2:
        st.metric("Positive", positive_reviews)

    with col3:
        st.metric("Negative", negative_reviews)

    with col4:
        st.metric("Neutral", neutral_reviews)
    st.markdown("---")

    # -----------------------------
    # CHARTS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sentiment Distribution")

        pie_chart = px.pie(
            sentiment_data,
            names="Sentiment",
            values="Count",
            hole=0.45
        )

        st.plotly_chart(
        pie_chart,
        width="stretch"
        )

    with col2:

        st.subheader("Review Breakdown")

        bar_chart = px.bar(
            bar_data,
            x="Category",
            y="Count"
        )

        st.plotly_chart(
        bar_chart,
        width="stretch"
        )

    # -----------------------------
    # PRAISES / COMPLAINTS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Praises")

        if uploaded_file is not None:
            for word, count in top_praises:
                if len(word) > 3:
                    st.success(f"{word} ({count})")

    with col2:

        st.subheader("Top Complaints")

        if uploaded_file is not None:
            for word, count in top_complaints:
                if len(word) > 3:
                    st.error(f"{word} ({count})")

    st.markdown("---")

    # -----------------------------
    # AI INSIGHTS
    # -----------------------------

    st.subheader("AI Insights")

    if uploaded_file is not None:
        st.info(ai_summary)

    else:
        st.info(
            "Upload a review dataset to generate AI-powered insights."
        )


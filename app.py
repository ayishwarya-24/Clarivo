import streamlit as st
import plotly.express as px
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

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
    st.write("Settings")

# -----------------------------
# HEADER
# -----------------------------

st.title("Clarivo Dashboard")

st.caption(
    "Monitor customer sentiment and discover actionable insights."
)

total_reviews = 0
positive_reviews = 0
negative_reviews = 0
neutral_reviews = 0

sentiment_data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Count": [0, 0, 0]
})

uploaded_file = st.file_uploader(
    "Upload Reviews CSV",
    type=["csv"]
)


if uploaded_file is not None:

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

    positive_text = " ".join(reviews_df[ reviews_df["Sentiment"] == "Positive"
    ]["Review"].astype(str))

    negative_text = " ".join(reviews_df[reviews_df["Sentiment"] == "Negative"
    ]["Review"].astype(str))

    positive_words = Counter(positive_text.lower().split())
    
    negative_words = Counter(negative_text.lower().split())
    
    top_praises = [
        (word, count)
        for word, count in positive_words.most_common()
        if word not in stop_words
    ]

    top_complaints = [
        (word, count)
        for word, count in negative_words.most_common()
        if word not in stop_words
    ]
    
    total_reviews = len(reviews_df)

    positive_reviews = len(reviews_df[reviews_df["Sentiment"] == "Positive"])
    
    negative_reviews = len(reviews_df[reviews_df["Sentiment"] == "Negative"])
    
    neutral_reviews = len(reviews_df[reviews_df["Sentiment"] == "Neutral"])

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

st.markdown("---")


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

st.info(
    """
    Customers are highly satisfied with sound quality and battery life.
    Most negative reviews mention Bluetooth connectivity and app stability.
    """
)

# -----------------------------
# REVIEWS TABLE
# -----------------------------

st.subheader("Recent Reviews")

if uploaded_file is not None:
    st.dataframe(
        reviews_df,
        width="stretch"
    )
else:
    st.info("Upload a CSV file to view reviews.")
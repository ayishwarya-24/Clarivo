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

st.markdown("""
<style>

div[data-testid="metric-container"] {
    background-color: #181818;
    border: 1px solid #2A2A2A;
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stHeaderActionElements"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "welcome"

# -----------------------------
# SAMPLE DATA
# -----------------------------


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

if st.session_state.page == "welcome":

    st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .hero-title {
    color: #F5F1D5;
    font-size: 110px;
    font-family: Georgia, serif;
    }

    .hero-subtitle {
    font-size: 28px;
    margin-top: 20px;
    color: #D7B46A;
    }

    .hero-description {
        font-size: 18px;
        color: #BDBDBD;
        line-height: 1.8;
    }

    .feature-card {
    background-color: #181818;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #2a2a2a;
    margin-bottom: 20px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 8px;
        color: #F5F1D5;
    }

    .feature-text {
        color: #BDBDBD;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='height:60px'></div>",
        unsafe_allow_html=True
    )

    left, right = st.columns([2, 1])

    with left:

        st.markdown(
            '<div class="hero-title">Clarivo</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-subtitle">Customer Feedback Intelligence Platform</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-description">
            Transform customer reviews into actionable insights using
            sentiment analysis, complaint detection and intelligent
            feedback analytics.
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Sentiment Analysis</div>
            <div class="feature-text">
            Automatically classify customer reviews as positive,
            neutral or negative.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Complaint Detection</div>
            <div class="feature-text">
            Identify recurring customer issues and pain points.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">AI Insights</div>
            <div class="feature-text">
            Generate actionable summaries from customer feedback.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])

    with col2:

        if st.button("NEXT", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()



if st.session_state.page == "dashboard":

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(
            """
            <h1 style="
                font-size:90px;
                color:#F4F1D8;
                font-family:Georgia, serif;
                margin-bottom:0;
            ">
                Clarivo
            </h1>

            <div style="
                color:#C8B273;
                font-size:22px;
                margin-top:-20px;
            ">
                Monitor customer sentiment and discover actionable insights.
            </div>
            """,
            unsafe_allow_html=True
        )
            

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("← Back", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()

    uploaded_file = st.file_uploader(
    "Upload Reviews CSV",
    type=["csv"]
    )

    if uploaded_file is None:
        st.info("Upload a review dataset to begin analysis.")

        st.markdown("---")

        st.caption(
        "CSV must contain a column named 'Review'."
        )

        # KPI placeholders
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Reviews", "--")

        with col2:
            st.metric("Positive Rate", "--")

        with col3:
            st.metric("Negative Rate", "--")

        with col4:
            st.metric("Overall Sentiment", "--")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Distribution")

            sample_pie = pd.DataFrame({
                "Sentiment": ["Positive", "Negative", "Neutral"],
                "Count": [1, 1, 1]
            })

            pie_chart = px.pie(
                sample_pie,
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

            sample_bar = pd.DataFrame({
                "Category": ["Positive", "Negative", "Neutral"],
                "Count": [1, 1, 1]
            })

            bar_chart = px.bar(
                sample_bar,
                x="Category",
                y="Count"
            )

            st.plotly_chart(
                bar_chart,
                width="stretch"
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

        positive_percent = round(
            (positive_reviews / total_reviews) * 100, 1
        )

        negative_percent = round(
            (negative_reviews / total_reviews) * 100, 1
        )

        neutral_percent = round(
            (neutral_reviews / total_reviews) * 100, 1
        )

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
        
        if positive_percent >= 70:
            health_score = "Excellent"
        elif positive_percent >= 50:
            health_score = "Good"
        elif positive_percent >= 30:
            health_score = "Fair"
        else:
            health_score = "Poor"

        strengths = ", ".join(positive_topics) if positive_topics else "No major strengths identified"

        issues = ", ".join(negative_topics) if negative_topics else "No major issues identified"

        if negative_percent > 40:
            recommendation = (
                "Customer dissatisfaction is high. Immediate attention should be given "
                "to recurring complaints to improve customer experience."
            )
        elif negative_percent > 20:
            recommendation = (
                "Some recurring issues were detected. Monitoring and corrective actions "
                "are recommended."
            )
        else:
            recommendation = (
                "Customer feedback is largely positive. Focus on maintaining strengths "
                "while continuing to monitor customer concerns."
            )

        
        ai_summary = f"""
        <b>Customer Health Score:</b> {health_score}<br>
        <b>Overall Sentiment:</b> {overall_sentiment}<br>
        <b>Key Strengths:</b> {strengths}<br>
        <b>Key Issues:</b> {issues}<br>
        <b>Recommendation:</b> {recommendation}
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

        csv_download = reviews_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Analyzed Reviews",
            data=csv_download,
            file_name="clarivo_analysis.csv",
            mime="text/csv"
        )



        # -----------------------------
        # KPI CARDS
        # -----------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Reviews",
                total_reviews
            )

        with col2:
            st.metric(
                "Positive Rate",
                f"{positive_percent}%"
            )


        with col3:
            st.metric(
                "Negative Rate",
                f"{negative_percent}%"
            )

        with col4:
            st.metric(
                "Overall Sentiment",
                overall_sentiment
            )

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
                y="Count",
                color="Category",
                color_discrete_map={
                    "Positive": "#2ECC71",
                    "Negative": "#E74C3C",
                    "Neutral": "#F1C40F"
                }
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
            st.markdown(f"""
            <div style="
                background-color:#151515;
                border:1px solid #2A2A2A;
                border-radius:18px;
                padding:18px;
            ">

            <h3 style="color:#C8B273;">
            Customer Intelligence Summary
            </h3>

            <div style="
                color:#F4F1D8;
                font-size:16px;
                line-height:1.6;
                font-family:Arial;
            ">
            {ai_summary.replace(chr(10), "<br>")}
            </div>

            </div>
            """, unsafe_allow_html=True)
                        


        st.markdown("---")

        st.markdown(
            """
            <div style="text-align:center;color:#888;">
                Clarivo • AI-Powered Customer Feedback Intelligence
                <br>
                Built with Streamlit, Pandas, Plotly and NLP
            </div>
            """,
            unsafe_allow_html=True
)

        



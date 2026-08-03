import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Clarivo",
    layout="wide"
)

# -----------------------------
# SAMPLE DATA
# -----------------------------

sentiment_data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Count": [892, 214, 142]
})

rating_data = pd.DataFrame({
    "Rating": ["5★", "4★", "3★", "2★", "1★"],
    "Count": [520, 280, 170, 90, 40]
})

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

st.markdown("---")

# -----------------------------
# KPI CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Reviews", "1,248")

with col2:
    st.metric("Positive", "892")

with col3:
    st.metric("Negative", "214")

with col4:
    st.metric("Neutral", "142")

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
        use_container_width=True
    )

with col2:

    st.subheader("Rating Distribution")

    bar_chart = px.bar(
        rating_data,
        x="Rating",
        y="Count"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# -----------------------------
# PRAISES / COMPLAINTS
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Praises")

    st.success("Battery Life")
    st.success("Sound Quality")
    st.success("Value for Money")

with col2:

    st.subheader("Top Complaints")

    st.error("Bluetooth Connectivity")
    st.error("Delivery Delays")
    st.error("App Crashes")

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

reviews = pd.DataFrame({
    "Rating": [5, 4, 2, 1],
    "Sentiment": ["Positive", "Positive", "Negative", "Negative"],
    "Review": [
        "Amazing battery life.",
        "Great value for money.",
        "Bluetooth disconnects often.",
        "App crashes constantly."
    ]
})

st.dataframe(
    reviews,
    use_container_width=True
)
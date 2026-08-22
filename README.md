# Clarivo

Transform Customer Feedback into Actionable Insights

Clarivo is an AI-powered customer feedback intelligence platform that helps businesses analyze customer reviews and discover actionable insights.

## Features

- Sentiment Analysis using NLP
- Customer Health Score
- AI-generated feedback summaries
- Complaint Detection
- Top Praises and Complaints Extraction
- Download Analyzed Results
- Visual Analytics with Plotly

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- VADER Sentiment Analysis

## How It Works

1. Upload a CSV file containing customer reviews.
2. Clarivo automatically classifies reviews as:
   - Positive
   - Neutral
   - Negative
3. The dashboard generates:
   - KPI metrics
   - Sentiment charts
   - Customer health score
   - AI-powered insights
4. Export the analyzed results.

## Dataset Format

Your CSV file should contain a column named:

```csv
Review
```

Example:

```csv
Review
Amazing battery life and sound quality
Bluetooth disconnects frequently
Excellent customer service
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ayishwarya-24/clarivo.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Future Improvements

- AI chatbot assistant
- Trend forecasting
- Multi-dataset comparison

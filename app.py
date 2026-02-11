import os
import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azure batch API limit: max 10 documents per request
AZURE_BATCH_LIMIT = 10

st.set_page_config(page_title="Sentiment Analysis")

load_dotenv()
key = os.getenv("AZURE_API_KEY")
my_endpoint = os.getenv("AZURE_ENDPOINT")

if not key or not my_endpoint:
    st.error("Missing Azure credentials. Please set AZURE_API_KEY and AZURE_ENDPOINT in your .env file.")
    st.stop()


@st.cache_resource
def authenticate_client():
    """Authenticate and return an Azure Text Analytics client.

    Returns:
        TextAnalyticsClient: An authenticated client instance.
    """
    key_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(
            endpoint=my_endpoint, 
            credential=key_credential)
    return client

def analyze_single(client, text):
    """Analyze sentiment for a single text string.

    Args:
        client: Authenticated Azure Text Analytics client.
        text: The text to analyze.

    Returns:
        dict: Sentiment label and positive, neutral, negative confidence scores.
    """
    try:
        response = client.analyze_sentiment(documents=[text])[0]
        return {
            "sentiment_result": response.sentiment,
            "positive_score": response.confidence_scores.positive,
            "neutral_score": response.confidence_scores.neutral,
            "negative_score": response.confidence_scores.negative
        }

    except Exception as err:
        st.error(f"Connection Failed: {err}")
        return {
            "sentiment_result": "Error",
            "positive_score": 0,
            "neutral_score": 0,
            "negative_score": 0
        }

def analyze_batch(client, texts):
    """Analyze sentiment for a list of texts, chunked to respect Azure's 10-doc limit.

    Args:
        client: Authenticated Azure Text Analytics client.
        texts: List of text strings to analyze.

    Returns:
        list[dict]: A list of sentiment results, one per input text.
    """
    all_results = []

    for i in range(0, len(texts), AZURE_BATCH_LIMIT):
        chunk = texts[i : i + AZURE_BATCH_LIMIT]
        try:
            response = client.analyze_sentiment(documents=chunk)
            for doc in response:
                if not doc.is_error:
                    all_results.append({
                        "sentiment_result": doc.sentiment,
                        "positive_score": doc.confidence_scores.positive,
                        "neutral_score": doc.confidence_scores.neutral,
                        "negative_score": doc.confidence_scores.negative
                    })
                else:
                    all_results.append({
                        "sentiment_result": "Error",
                        "positive_score": 0,
                        "neutral_score": 0,
                        "negative_score": 0,
                        "error_detail": f"{doc.error.code}: {doc.error.message}"
                    })
        except Exception as err:
            st.error(f"Batch analysis failed: {err}")
            all_results.extend([{
                "sentiment_result": "Error",
                "positive_score": 0,
                "neutral_score": 0,
                "negative_score": 0
            }] * len(chunk))

    return all_results

def file_analysis(uploaded_file, client, max_rows):
    """Read an uploaded CSV/Excel file and run batch sentiment analysis.

    Args:
        uploaded_file: Streamlit UploadedFile object (.csv or .xlsx).
        client: Authenticated Azure Text Analytics client.
        max_rows: Maximum number of rows to analyze.

    Returns:
        DataFrame with sentiment results appended, or None on failure.
    """
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
            else:
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file)

            if 'ID' not in df.columns or 'review_text' not in df.columns:
                st.error("Please use the template file")
                return None

            clean_df = df[['ID', 'review_text']].head(max_rows).copy()

            # Sanitize: drop empty / whitespace-only / NaN rows
            clean_df['review_text'] = clean_df['review_text'].astype(str).str.strip()
            clean_df = clean_df[clean_df['review_text'].ne('') & clean_df['review_text'].ne('nan')]

            if clean_df.empty:
                st.warning("No valid review text found after filtering empty rows.")
                return None

            text_list = clean_df['review_text'].tolist()

            with st.spinner(f"Analyzing {len(text_list)} rows..."):
                batch_results = analyze_batch(client, text_list)
            
            if batch_results:
                sentiment_df = pd.DataFrame(batch_results)
                final_df = pd.concat([clean_df.reset_index(drop=True), sentiment_df], axis=1)
                return final_df

            return None

        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    return None
    


if __name__ == "__main__":
    st.header("Sentiment Analysis With Azure Text Analytics")
    st.markdown(" ")
    st.subheader("Welcome! Enter a sentence or upload a file to start.")

    
    st.markdown("""
    <style>
    div[data-baseweb="tab-list"] {
        display: flex;
        width: 100%;}

div[data-baseweb="tab-list"] > button {flex: 1;}

    /* Style the Analyze buttons with red background */
    button[kind="primary"] {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        background-color: #e03e3e !important;
        border-color: #e03e3e !important;
    }
    </style>
    """, unsafe_allow_html=True)

    azure_client = authenticate_client()

    tab_text, tab_file = st.tabs(["Analyze Text", "Analyze File"])

    with tab_text:
        my_text_area = st.text_area("Enter your text:", height=160, placeholder="Enter text to analyze...")
        if st.button("Analyze", key="btn_text", type="primary", use_container_width=True):
            if my_text_area.strip() != "":
                st.table(analyze_single(azure_client, my_text_area))
            else:
                st.warning("Please enter a sentence to analyze.")

    with tab_file:
        file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
        max_rows = st.slider("Max rows to analyze", min_value=1, max_value=10, value=1, step=1)

        # Side-by-side buttons: Download | Analyze
        col1, col2 = st.columns(2)
        with col1:
            template_path = os.path.join(os.path.dirname(__file__), "data", "sample_reviews.csv")
            if os.path.exists(template_path):
                with open(template_path, "rb") as tpl:
                    st.download_button(
                        "Download Template CSV",
                        data=tpl,
                        file_name="sample_reviews.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
        with col2:
            analyze_clicked = st.button("Analyze", key="btn_file", type="primary", use_container_width=True)

        if analyze_clicked:
            if file:
                result_df = file_analysis(file, azure_client, max_rows)
                if result_df is not None:
                    st.dataframe(result_df, hide_index=True)

                    # Metric Cards 
                    total = len(result_df)
                    pos_count = int((result_df["sentiment_result"] == "positive").sum())
                    neu_count = int((result_df["sentiment_result"] == "neutral").sum())
                    neg_count = int((result_df["sentiment_result"] == "negative").sum())

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Total Reviews", total)
                    m2.metric("Positive", pos_count)
                    m3.metric("Neutral", neu_count)
                    m4.metric("Negative", neg_count)

                    # Donut Chart
                    sentiment_counts = (
                        result_df["sentiment_result"]
                        .value_counts()
                        .reset_index()
                    )
                    sentiment_counts.columns = ["Sentiment", "Count"]

                    color_scale = alt.Scale(
                        domain=["positive", "neutral", "negative"],
                        range=["#2ecc71", "#95a5a6", "#e74c3c"],
                    )

                    donut = (
                        alt.Chart(sentiment_counts)
                        .mark_arc(innerRadius=60)
                        .encode(
                            theta=alt.Theta("Count:Q"),
                            color=alt.Color("Sentiment:N", scale=color_scale),
                            tooltip=["Sentiment", "Count"],
                        )
                        .properties(title="Sentiment Distribution", height=350)
                    )

                    st.altair_chart(donut, use_container_width=True)
            else:
                st.warning("Please upload a file.")
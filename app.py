import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

#to get the Azure key and endpoint from .env file
load_dotenv()
key = os.getenv("AZURE_API_KEY")
my_endpoint = os.getenv("AZURE_ENDPOINT")


#function to authenticate the client
def authenticate_client():
    keyObject = AzureKeyCredential(key)
    client = TextAnalyticsClient(
            endpoint=my_endpoint, 
            credential=keyObject)
    return client

#function to perform sentiment analysis
def sentiment_analysis(client, text):
    global sentiment_result, positive_score, neutral_score, negative_score
    try:
        response = client.analyze_sentiment(documents=[text])[0]
        sentiment_result= response.sentiment 
        positive_score = response.confidence_scores.positive
        neutral_score = response.confidence_scores.neutral
        negative_score = response.confidence_scores.negative

    except Exception as err:
        print(f"Connection Failed: {err}")

if __name__ == "__main__":
    st.header("Sentiment Analysis With Azure Text Analytics")
    st.markdown(" ")
    st.subheader("Welcome! Please upload your sentence or an Excel file to start.")
        
    col1, col2 = st.columns(2)
    with col1:
        my_text_area = st.text_area("Sentence Analysis:", height=160, placeholder="Type your sentence here...")
    with col2:
        file = st.file_uploader("Choose a file (TODO)", type=["cvs", "xlsx"])
    
    st.radio("Select the input type: (TODO)", ("Sentence", "Excel File"))

    if st.button("Analyze"):
        if my_text_area.strip() != "":
            sentiment_analysis(authenticate_client(),my_text_area)
            st.table(
           {"Sentiment": sentiment_result,
            "Positive Score": positive_score,
            "Neutral Score": neutral_score,
            "Negative Score": negative_score})
        else:
            st.warning("Please enter a sentence to analyze.")

    
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

#function to handle the files
def file_analysis(uploaded_file, client):
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

            clean_df = df[['ID', 'review_text']].head(10).copy()
            
            st.info("Analyzing the first 10 rows...")

            sentiment_data = clean_df['review_text'].apply(
                lambda x: pd.Series(sentiment_analysis(client, x))
            )
            
            final_df = pd.concat([clean_df, sentiment_data], axis=1)

            return final_df

        except Exception as e:
            st.error("Error reading file")
            return None
    return None    
    


if __name__ == "__main__":
    st.header("Sentiment Analysis With Azure Text Analytics")
    st.markdown(" ")
    st.subheader("Welcome! Please upload your sentence or an Excel file to start.")
        
    col1, col2 = st.columns(2)
    with col1:
        my_text_area = st.text_area("Sentence Analysis:", height=160, placeholder="Type your sentence here...")
    with col2:
        file = st.file_uploader("Choose a file (the resault is limited to 10 records only)", type=["csv", "xlsx"])
    
    choice = st.radio("Select the input type:", ("Sentence", "Excel File"))
    analyzebutton = st.button("Analyze")
    
    if analyzebutton:
        if choice=="Sentence":
            
            if my_text_area.strip() != "":
                st.table(sentiment_analysis(authenticate_client(), my_text_area))
            else:
                st.warning("Please enter a sentence to analyze.")
        
    
        if choice=="Excel File":
            if file:
                resault_df= file_analysis(file, authenticate_client())
                if resault_df is not None:
                    st.write(resault_df)
                else:
                    st.warning("Please upload a file")


    
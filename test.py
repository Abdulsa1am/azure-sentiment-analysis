import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
key = os.getenv("my_key")
my_endpoint = os.getenv("my_endpoint")

def authenticate_client():
    keyObject = AzureKeyCredential(key)
    client = TextAnalyticsClient(
            endpoint=my_endpoint, 
            credential=keyObject)
    return client

def sentiment_analysis_example(client):
    try:
        text = ["I am so happy"]
        response = client.analyze_sentiment(documents=text)[0] #0 for only one text input (it will return only 1 output)
        print(f"Document Sentiment: {response.sentiment}") #final resault 
        
        print(f"Overall scores: positive={response.confidence_scores.positive}, "
              f"neutral={response.confidence_scores.neutral}, "
              f"negative={response.confidence_scores.negative}")
        print("Job done")
    except Exception as err:
        print(f"Connection Failed: {err}")

if __name__ == "__main__":
    testclient = authenticate_client()
    sentiment_analysis_example(testclient)
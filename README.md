# Azure Sentiment Analysis

A Streamlit web app that performs sentiment analysis using the **Azure AI Text Analytics** API.

## Features

- Analyze a single sentence for sentiment (positive / neutral / negative).
- Upload a CSV or Excel file to batch-analyze up to 10 reviews.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure credentials

Create a `.env` file in the project root:

```
AZURE_API_KEY=your_azure_key_here
AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
```

You can obtain these from the [Azure Portal](https://portal.azure.com/) under your **Text Analytics** resource → **Keys and Endpoint**.

### 3. Run the app

```bash
streamlit run app.py
```

## File Upload Format

Upload a `.csv` or `.xlsx` file with these columns:

| ID  | review_text          |
| --- | -------------------- |
| 1   | I love this product! |
| 2   | Terrible experience. |

## Limitations

- File analysis is limited to the first **10 rows**.
- Requires an active Azure AI Text Analytics resource.
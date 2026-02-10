# Azure Sentiment Analysis with Streamlit

A web-based sentiment analysis application that leverages Azure AI Text Analytics to analyze sentiment in text and Excel files. Built with Streamlit for an intuitive and interactive user experience.

## Features

- **Real-time Sentiment Analysis**: Analyze sentiment of text input instantly
- **Batch Processing**: Upload CSV or Excel files for bulk sentiment analysis
- **Confidence Scores**: Get detailed confidence scores for positive, neutral, and negative sentiments
- **Interactive Web Interface**: User-friendly Streamlit interface for easy interaction
- **Multi-format Support**: Process individual sentences or upload CSV/XLSX files
- **Visual Results**: Display sentiment analysis results in clear, tabular format

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.7+**: Python installed on your system
- **Azure Account**: An active Azure subscription
- **Azure Text Analytics Resource**: 
  - Create a Text Analytics resource in the Azure Portal
  - Obtain your API key and endpoint URL

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abdulsa1am/azure-sentiment-analysis.git
   cd azure-sentiment-analysis
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```bash
   touch .env
   ```
   
   Add your Azure credentials to the `.env` file:
   ```env
   AZURE_API_KEY=your_azure_api_key_here
   AZURE_ENDPOINT=your_azure_endpoint_here
   ```
   
   Replace `your_azure_api_key_here` and `your_azure_endpoint_here` with your actual Azure Text Analytics credentials.

## Usage

1. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   
   Open your web browser and navigate to `http://localhost:8501`

3. **Analyze sentiment**
   
   **Option 1: Single Sentence Analysis**
   - Enter your text in the "Sentence Analysis" text area
   - Select "Sentence" as the input type
   - Click the "Analyze" button
   - View the sentiment results with confidence scores

   **Option 2: File Analysis**
   - Prepare a CSV or XLSX file with the following structure:
     ```
     ID,review_text
     1,"This product is amazing!"
     2,"Not satisfied with the service"
     3,"It's okay, nothing special"
     ```
   - Upload the file using the file uploader
   - Select "Excel File" as the input type
   - Click the "Analyze" button
   - View the sentiment analysis for the first 10 rows

## Project Structure

```
azure-sentiment-analysis/
│
├── app.py                 # Main Streamlit application
├── azure_service.py       # Azure Text Analytics service utilities
├── test.py                # Test script for Azure connection
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not tracked in git)
├── .gitignore            # Git ignore file
├── data/                 # Sample data files
│   └── sample_reviews.csv
└── README.md             # Project documentation
```

### File Descriptions

- **app.py**: The main application file containing the Streamlit UI and sentiment analysis logic
- **azure_service.py**: Additional Azure service utilities (currently minimal)
- **test.py**: Test script to verify Azure Text Analytics connection
- **requirements.txt**: Lists all Python package dependencies
- **data/**: Contains sample CSV files for testing the file upload feature

## How It Works

1. The application authenticates with Azure Text Analytics using credentials from the `.env` file
2. User input (text or file) is processed through the Azure Text Analytics API
3. The API returns sentiment classification (Positive, Neutral, or Negative) along with confidence scores
4. Results are displayed in a user-friendly format in the Streamlit interface

## Example Output

When analyzing text, you'll receive:
- **Sentiment Result**: The overall sentiment (positive, neutral, or negative)
- **Positive Score**: Confidence score for positive sentiment (0-1)
- **Neutral Score**: Confidence score for neutral sentiment (0-1)
- **Negative Score**: Confidence score for negative sentiment (0-1)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

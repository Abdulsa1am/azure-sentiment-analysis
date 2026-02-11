# Azure Sentiment Analysis

A **Streamlit** web application that performs real-time sentiment analysis using the **Azure AI Text Analytics** API. Analyze individual sentences or batch-process reviews from CSV/Excel files.

---

## Features

- **Single Text Analysis** — Enter any sentence and instantly receive sentiment classification (positive, neutral, or negative) along with confidence scores.
- **Batch File Analysis** — Upload a `.csv` or `.xlsx` file to analyze up to 10 reviews per API call, with automatic chunking for larger datasets.
- **Downloadable Template** — A ready-made `sample_reviews.csv` template is included so you can get started quickly.
- **Tabbed Interface** — Clean, tab-based UI separating text and file analysis workflows.

---

## Tech Stack

| Layer       | Technology                  |
| ----------- | --------------------------- |
| Frontend    | Streamlit                   |
| AI Service  | Azure sentiment analysis    |
| Data        | Pandas, OpenPyXL            |
| Environment | python-dotenv               |

---

## Getting Started

### Prerequisites

- **Python 3.9+**
- An active **Azure AI Text Analytics** resource ([create one here](https://portal.azure.com/))

### 1. Clone the repository

```bash
git clone https://github.com/Abdulsa1am/azure-sentiment-analysis.git
cd azure-sentiment-analysis
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure credentials

Create a `.env` file in the project root:

```env
AZURE_API_KEY=your_azure_key_here
AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
```

> You can find these values in the [Azure Portal](https://portal.azure.com/) under your **Text Analytics** resource → **Keys and Endpoint**.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

---

## File Upload Format

Upload a `.csv` or `.xlsx` file containing the following columns:

| ID  | review_text          |
| --- | -------------------- |
| 1   | I love this product! |
| 2   | Terrible experience. |

A sample template is available at [`data/sample_reviews.csv`](data/sample_reviews.csv) or via the **Download Template CSV** button inside the app.

---

## Project Structure

```
azure-sentiment-analysis/
├── app.py               # Main Streamlit application
├── data/
│   └── sample_reviews.csv   # Template file for batch analysis
├── requirements.txt     # Pinned Python dependencies
├── .env                 # Azure credentials (git-ignored)
├── .gitignore
└── README.md
```

---

## Limitations

- Each Azure API call is limited to **10 documents**; larger files are automatically chunked.
- Requires an active **Azure AI Text Analytics** resource with a valid API key.
- Empty or whitespace-only review rows are automatically filtered out before analysis.

---

## License

This project is open-source. Feel free to use and modify it as needed.
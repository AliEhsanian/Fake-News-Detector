# Fake News Detector

A Streamlit-based web application that analyzes news headlines and claims for credibility using web scraping and AI.

## Features

- **Web Search Integration**: Automatically searches Google for relevant information and sources
- **AI-Powered Analysis**: Uses LLMs to evaluate claim credibility
- **Comprehensive Scoring**: Provides detailed credibility scores (0-10) with confidence levels
- **Multi-Factor Analysis**: Examines key findings, red flags, and supporting evidence
- **Source Transparency**: Displays all sources used in the analysis

## Project Structure

```
fake-news-detector/
│
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── config.py           # Configuration management
│   ├── scraper.py          # Web scraping module
│   ├── analyzer.py         # AI analysis module
│   ├── utils.py            # Utility functions
│   └── images/
│       └── banner.png      # App banner image
│
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
└── README.md              # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (or compatible API)
- Google Custom Search API credentials (optional but recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AliEhsanian/fake-news-detector.git
   cd fake-news-detector
   ```

2. **Install dependencies**
   ```bash
   uv install
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   # Required: OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here

   # Google Search API (recommended)
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_custom_search_engine_id

   # Optional: Configuration
   MAX_SEARCH_RESULTS=5
   SEARCH_TIMEOUT=10
   MODEL_NAME=gpt-5-nano
   MAX_TOKENS=1000
   TEMPERATURE=0.8
   ```

## Usage

1. Run the Streamlit app:
```bash
uv run streamlit run src/app.py
```
or
```bash
streamlit run src/app.py
```

2. Open your browser to `http://localhost:8501`

3. Enter a news headline or claim to verify

4. Click "Analyze" to get the credibility assessment

## How It Works

1. **Input**: Enter a news headline or claim to verify
2. **Search**: The app searches Google for relevant information about the claim
3. **Analysis**: AI analyzes the search results for credibility indicators
4. **Results**: Receive a detailed breakdown including:
   - Credibility score (0-10)
   - Verdict (Likely True/False/Uncertain/Mixed Evidence)
   - Confidence level (High/Medium/Low)
   - Key findings and evidence
   - Red flags and supporting evidence
   - Source links for verification

## Configuration Options

You can customize the app behavior through environment variables:

### LLM Configuration

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: OpenAI model to use (default: gpt-3.5-turbo)
- `TEMPERATURE`: Model temperature for analysis (0.0-1.0)
- `MAX_TOKENS`: Maximum tokens for response (default: 1000)

### Search Configuration
- `GOOGLE_API_KEY`: Your Google Custom Search API key for web searches
- `GOOGLE_CSE_ID`: Your Custom Search Engine ID from Google
- `MAX_SEARCH_RESULTS`: Number of search results to analyze (default: 5)
- `SEARCH_TIMEOUT`: Maximum time in seconds to wait for search results (default: 10)

## Troubleshooting

### Common Issues

**Issue**: "Please configure your OpenAI API key"
- **Solution**: Ensure `OPENAI_API_KEY` is set in `.env` file

**Issue**: "Could not retrieve search results"
- **Solution**: Check Google API credentials or increase `SEARCH_TIMEOUT`

**Issue**: API rate limit exceeded
- **Solution**: Wait or upgrade to paid tier for higher limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is designed to assist with fact-checking but should not be considered the sole source of truth. Always verify information through multiple reliable sources and exercise critical thinking. The AI's analysis is based on available search results and may not always be accurate or complete.

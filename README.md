# Google Maps Screenshot Analysis Tool

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Groq API Key:
- Open `.env` file
- Replace `your_groq_api_key_here` with your actual Groq API key

## Usage
```bash
python main.py "https://www.google.com/maps/place/example_location"
```

## Dependencies
- Selenium WebDriver
- Pillow (PIL)
- Groq API
- python-dotenv

## Notes
- Requires Chrome/Chromium browser installed
- Headless browser used for screenshot
- Screenshot of left third of map will be processed

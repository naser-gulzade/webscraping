# Web Scraping API

This project is a web API solution designed to scrape websites based on a provided sitemap URL. It gathers all root domain URLs and returns the title, content, and URL in JSON format to specified webhooks.

## Project Structure

```
web-scraping-api
├── src
│   ├── main.py          # Entry point of the application
│   ├── scraper.py       # Contains the Scraper class for web scraping
│   └── utils
│       └── __init__.py  # Utility functions for the scraper
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/web-scraping-api.git
   cd web-scraping-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the API, execute the following command:
```
uvicorn src.main:app --reload
```

### API Endpoint

- **GET /scrape**
  
  This endpoint accepts a sitemap URL and a webhook URL as query parameters.

  **Parameters:**
  - `sitemap_url`: The URL of the sitemap to scrape.
  - `webhook_url`: The URL to which the scraped data will be sent.

  **Example Request:**
  ```
  GET /scrape?sitemap_url=https://example.com/sitemap.xml&webhook_url=https://yourwebhook.com
  ```

## Dependencies

- FastAPI
- requests
- BeautifulSoup4
- uvicorn

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
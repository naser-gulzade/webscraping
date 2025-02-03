# Web Scraping API

This project is a web API solution designed to scrape websites based on a provided sitemap URL. It gathers all root domain URLs and returns the title, content, and URL in JSON format to specified webhooks.

This web scraper check if the urls is bigger than 10 items then it will run in background thread (job) and return to the webhooks

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
   git clone https://github.com/naser-gulzade/webscraping.git
   cd webscraping
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

- **GET /scrape-geturls?urls=**
  
  This endpoint accepts a urls in comma separated values e.g. urls=http//example.com, http//example.org

  **Parameters:**
  - `urls`: The URL of the sitemap to scrape.

  **Example Request:**
  ```
  GET /scrape-geturls?urls=https://example.com/sitemap.xml&webhook_url=https://yourwebhook.com
  ```

- **GET /get-sitemap-urls?sitemap_url=**

  This endpoint accepts a sitemap URL and returns all URLs found in the sitemap that are within the same domain.

  **Parameters:**
  - `sitemap_url`: The URL of the sitemap to parse.

  **Example Request:**
  ```
  GET /get-sitemap-urls?sitemap_url=https://example.com/sitemap.xml
  ```

- **POST /scrape-urls**

This endpoint accepts a JSON payload with a list of URLs and a webhook as optional to scrape.

**Payload:**
```json
{
  "urls": ["https://example.com", "https://example.org"],
  "webhook_url": "https://example.com"
}

**Example Request:**
 ```
POST /scrape-urls
Content-Type: application/json

{
  "urls": ["https://example.com", "https://example.org"],
  "webhook_url": "https://example.com/webhook"
}

- **POST /scrape-by-sitemap**

This endpoint accepts a JSON payload with a list of sitemap and webhook-url optional.

**Payload:**
```json
{
  "sitemaps": ["https://example.com/sitemap1.xml", "https://example.org/sitemap2.xml"],
  "webhook_url"
}

**Example Request:**
POST /scrape-by-sitemaps
Content-Type: application/json

{
  "sitemaps": ["https://example.com/sitemap.xml", "https://example.org/sitemap.xml"],
  "webhook_url": "https://example.com/webhook"
}



## Dependencies

- FastAPI
- requests
- BeautifulSoup4
- uvicorn

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
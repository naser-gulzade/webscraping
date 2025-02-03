from fastapi import FastAPI, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from .scraper import Scraper
from typing import List, Optional


app = FastAPI()

    
@app.get("/scrape-geturls")
async def scrape_geturls(urls: str = Query(...)):
    scraper = Scraper()
    url_list = urls.split(',')
    results = scraper.scrape_urls_get(url_list)
    return JSONResponse(content=results)    


# Define a Pydantic model for the JSON payload
class UrlPayload(BaseModel):
    urls: List[str]
    webhook_url: Optional[HttpUrl] = None  # Optional webhook URL

class SitemapPayload(BaseModel):
    sitemaps: List[HttpUrl]  # List of sitemap URLs
    webhook_url: Optional[HttpUrl] = None  # Optional webhook URL

@app.post("/scrape-urls")
async def scrape_urls(payload: UrlPayload):
    """
    Accepts a JSON payload with a list of URLs and scrapes them.

    Args:
        payload (UrlPayload): A JSON payload containing a list of URLs.

    Returns:
        JSONResponse: The results of scraping the URLs.
    """
    scraper = Scraper(payload.webhook_url)
    results = scraper.scrape_urls(payload.urls)
    return JSONResponse(content=results)

@app.get("/get-sitemap-urls")
async def get_sitemap_urls(sitemap_url: str):
    """
    Retrieves all URLs from the given sitemap URL that are within the same domain.

    Args:
        sitemap_url (str): The URL of the sitemap to parse.

    Returns:
        JSONResponse: A list of URLs found in the sitemap or an error message.
    """
    scraper = Scraper()
    urls = scraper.get_urls_from_sitemap(sitemap_url)
    return JSONResponse(content=urls)


@app.post("/scrape-by-sitemap")
async def scrape_by_sitemap(payload: SitemapPayload):
    """
    Accepts a JSON payload with a list of sitemaps and scrapes them.

    Args:
        payload (UrlPayload): A JSON payload containing a list of sitemaps.

    Returns:
        JSONResponse: The results of scraping the URLs.
    """
    scraper = Scraper(payload.webhook_url)

    # Get all URLs from the sitemaps
    urls = []
    for sitemap in payload.sitemaps:
        urls.extend(scraper.get_urls_from_sitemap(sitemap))

    # Scrape the URLs
    results = scraper.scrape_urls(urls)
    return JSONResponse(content=results)

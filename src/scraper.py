import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor

class Scraper:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url

    def scrape_urls_get(self, urls):
        if isinstance(urls, str):
            urls = [urls]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        results = []
        for url in urls:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else 'No title'
                content = soup.get_text()
                results.append({
                    'url': url,
                    'title': title,
                    'content': content
                })
            else:
                results.append({
                    'url': url,
                    'error': f'Failed to retrieve content, status code: {response.status_code}'
                })
        return results
    

    def get_urls_from_sitemap(self, sitemap_url):
        """
        Retrieves all URLs from the given sitemap URL that are within the same domain.

        Args:
            sitemap_url (str): The URL of the sitemap to parse.

        Returns:
            list: A list of URLs found in the sitemap or an error message.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(sitemap_url, headers=headers)
        if response.status_code != 200:
            return {'error': f'Failed to retrieve sitemap, status code: {response.status_code}'}

        soup = BeautifulSoup(response.content, 'xml')
         # Find only <loc> tags that are direct children of <url>
        urls = [loc.text for loc in soup.find_all('loc') if loc.find_parent('url')]
        # Filter out image URLs
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        filtered_urls = [
            url for url in urls
            if not any(url.lower().endswith(ext) for ext in image_extensions)
        ]

        return filtered_urls
    
    def scrape_urls(self, urls):
        """
        Scrapes the given list of URLs and returns their titles and content.
        If more than 10 URLs, it runs in the background and sends results to a webhook.
        """
        if isinstance(urls, str):
            urls = [urls]

        # If more than 10 URLs, run in background
        if len(urls) > 10 and self.webhook_url:
            threading.Thread(target=self._scrape_and_send, args=(urls,)).start()
            return {"status": "Processing in background", "message": "Results will be sent to webhook."}
        else:
            return self._scrape(urls)


    def _scrape(self, urls):
        """Scrape URLs synchronously and return results."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self._fetch_url, url, headers): url for url in urls}
            for future in future_to_url:
                results.append(future.result())

        return results

    def _fetch_url(self, url, headers):
        """Fetch and parse a single URL."""
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else 'No title'
            content = soup.get_text()
            return {'url': url, 'title': title, 'content': content}
        else:
            return {'url': url, 'error': f'Failed to retrieve content, status code: {response.status_code}'}

    def _scrape_and_send(self, urls):
        """Scrapes URLs in the background and sends data to the webhook."""
        results = self._scrape(urls)
        if self.webhook_url:
            requests.post(self.webhook_url, json={'data': results})
        print("Background scraping completed, data sent to webhook.")
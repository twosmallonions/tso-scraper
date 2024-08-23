import httpx
from recipe_scrapers import AbstractScraper, scrape_html


async def scrape(url: str, html: str) -> AbstractScraper:
    return scrape_html(html, org_url=url, supported_only=False, online=True)


async def download(url: str, http_client: httpx.AsyncClient) -> str:
    return (await http_client.get(url)).text

import json
import logging
import os
from datetime import timedelta
from typing import Any
from urllib.parse import urlparse

import httpx
import redis.asyncio as redis
from recipe_scrapers import scrape_html

REDIS_HOST = os.environ['SCRAPER_REDIS_HOST']
REDIS_PORT = os.environ['SCRAPER_REDIS_PORT']
HTTP_USER_AGENT = os.environ.get('SCRAPER_USER_AGENT', 'tso-scraper/0.1')


class RecipeScrapers:
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient(
            http2=True,
            timeout=httpx.Timeout(10.0),
            follow_redirects=True,
            max_redirects=5,
            headers={'user-agent': HTTP_USER_AGENT},
        )
        self.redis_client = redis.Redis(
            host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True
        )

    async def scrape(self, url: str) -> dict[str, Any]:
        parsed_url = urlparse(url)
        cache_key = parsed_url.netloc + parsed_url.path

        cached_recipe = await self.redis_client.get(cache_key)
        if cached_recipe is not None:
            logging.debug('Cache hit for %s', url)
            return json.loads(cached_recipe)

        try:
            recipe_html = (await self.http_client.get(url)).text
        except httpx.HTTPError:
            logging.info('HTTPError while fetching recipe')
            raise
        recipe = scrape_html(recipe_html, url, supported_only=False)
        recipe_json = recipe.to_json()
        await self.redis_client.setex(cache_key, timedelta(minutes=10), json.dumps(recipe_json))
        return recipe_json

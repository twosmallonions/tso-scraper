import json
from typing import Annotated, Any

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

from tso_scraper.dependencies import auth, http_client, redis_client as redis_client_dependency
from tso_scraper.scrape import service

router = APIRouter(prefix='/scrape')


@router.get('/', response_model=None)
async def scrape(
    _: Annotated[None, Depends(auth)],
    url: HttpUrl,
    http: Annotated[httpx.AsyncClient, Depends(http_client)],
    redis_client: Annotated[redis.Redis, Depends(redis_client_dependency)],
    raw: bool = False,  # noqa: FBT001, FBT002
) -> JSONResponse | Response:
    cache_key = f'{url.host}:{url.path}'
    cache_key_raw = f'{cache_key}:raw'
    if raw:
        html_cached = await redis_client.get(cache_key_raw)
        if html_cached is not None:
            return Response(content=html_cached.decode(), status_code=200, media_type='text/plain')

    recipe_cached: bytes | None = await redis_client.get(cache_key)
    if recipe_cached is not None and not raw:
        return JSONResponse(content=json.loads(recipe_cached))

    html = await service.download(str(url), http)
    await redis_client.setex(cache_key_raw, 3600, html)
    if raw:
        return Response(content=html, status_code=200, media_type='text/plain')
    scraper = await service.scrape(str(url), html)

    recipe_json: dict[Any, Any] = scraper.to_json()

    await redis_client.setex(cache_key, 3600, json.dumps(recipe_json))
    return JSONResponse(content=recipe_json)

from collections.abc import AsyncGenerator
from typing import Annotated

import httpx
import redis.asyncio as redis
from fastapi import HTTPException, Header
from fastapi.security import OpenIdConnect

from tso_scraper.cache import redis_pool
from tso_scraper.config import config

oidc = OpenIdConnect(
    openIdConnectUrl='http://localhost:8080/realms/tso/.well-known/openid-configuration',
    auto_error=True,
)


async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client


def redis_client() -> redis.Redis:
    return redis.Redis.from_pool(redis_pool)


AUTH_HEADER_PARTS = 2


def auth(authorization: Annotated[str, Header()]):
    split = authorization.split(' ')
    if len(split) != AUTH_HEADER_PARTS:
        raise HTTPException(status_code=401)

    secret = split[1]
    if not secret == config.secret:
        raise HTTPException(status_code=401)

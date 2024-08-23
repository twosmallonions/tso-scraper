import redis.asyncio as redis

redis_pool = redis.ConnectionPool.from_url('redis://localhost:6380')  # type: ignore

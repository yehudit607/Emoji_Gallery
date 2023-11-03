import aioredis

async def get_redis():
    # You might want to externalize the URI to configuration files or environment variables.
    redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
    return redis
import redis.asyncio as aioredis
from config import settings


async def get_redis():
    redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_POST}",db=settings.REDIS_DB)
    try:
        yield redis
    finally:
        await redis.close()

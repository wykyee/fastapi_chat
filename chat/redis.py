import aioredis

from settings import get_broker_settings


async def connect_redis() -> aioredis.Redis:
    settings = get_broker_settings()
    return await aioredis.create_redis(f"redis://{settings.host}:{settings.port}")

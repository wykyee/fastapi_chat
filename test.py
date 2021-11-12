import asyncio
import json
import aioredis
from settings import get_broker_settings


async def test():
    settings = get_broker_settings()
    redis = aioredis.from_url(f"redis://{settings.host}:{settings.port}")
    data = json.dumps({"id": 1, "body": "text", "author": {"id": 1, "name": "Test author"}})
    await redis.publish(settings.channel_name, data)


if __name__ == "__main__":
    asyncio.run(test())

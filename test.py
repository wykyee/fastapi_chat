import asyncio
import json
import aioredis
from settings import get_broker_settings


async def test():
    settings = get_broker_settings()
    pub = await aioredis.create_redis(f"redis://{settings.host}:{settings.port}")
    data = json.dumps(
        {"sender_id": 2, "receiver_ids": [1], "message": {"id": 1, "body": "text", "author": {"id": 1, "name": "Test author"}}}
    ).encode("utf-8")
    print(data)

    await pub.publish(settings.channel_name, data.decode())


if __name__ == "__main__":
    asyncio.run(test())

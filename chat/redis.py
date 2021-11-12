from typing import Union

import aioredis


async def connect_redis(host: str, port: Union[str, int]) -> aioredis.Redis:
    redis = await aioredis.from_url(f"redis://{host}:{port}")
    return redis


async def subscribe_channel(redis: aioredis.Redis, channel_name: str) -> aioredis.client.PubSub:
    channel = redis.pubsub()
    await channel.subscribe(channel_name)
    return channel

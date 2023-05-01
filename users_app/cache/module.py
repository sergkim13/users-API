import json

from aioredis.client import Redis
from fastapi.encoders import jsonable_encoder

from users_app.cache.abstract_cache import AbstractCache
from users_app.cache.settings import EXPIRE_TIME, redis_client


class RedisCache(AbstractCache):
    def __init__(self, cache_client: Redis) -> None:
        self.redis_client = cache_client

    async def get(self, key: str):
        value = await self.redis_client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: str, expire_time=EXPIRE_TIME):
        value = json.dumps(jsonable_encoder(value))
        await self.redis_client.set(key, value, expire_time)

    async def clear(self, key: str):
        if key == 'all':
            async for key in self.redis_client.scan_iter('users-*'):
                await self.redis_client.delete(key)
        else:
            await self.redis_client.delete(key)


def get_cache():
    return RedisCache(cache_client=redis_client)

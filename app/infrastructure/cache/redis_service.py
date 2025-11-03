from typing import Optional

from app.domain.services.cache import ICache
from app.domain.services.cache_client import ICacheClient


class RedisService(ICache):
    def __init__(
            self, redis: ICacheClient,
    ):
        self.redis = redis.get_client()

    async def set(self, key: str, value: str, ex=None) -> None:
        if ex:
            await self.redis.set(key, value, ex)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        result = await self.redis.exists(key)
        return bool(result)

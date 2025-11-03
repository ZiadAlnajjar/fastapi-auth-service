import logging
from typing import Optional

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    _pool: Optional[redis.ConnectionPool] = None
    _client: Optional[redis.Redis] = None

    @classmethod
    async def init(cls) -> None:
        if cls._pool is None:
            logger.info("Initializing Redis connection pool...")

            cls._pool = redis.ConnectionPool.from_url(
                settings.cache_url, decode_responses=True
            )
            cls._client = redis.Redis(connection_pool=cls._pool)

            try:
                pong = await cls._client.ping()
                if pong:
                    logger.info("Redis connected successfully")
            except Exception as e:
                logger.critical(f"Failed to connect to Redis: {e}")
                raise

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            raise RuntimeError("Redis client not initialized. Call RedisClient.init() first.")
        return cls._client

    @classmethod
    async def close(cls) -> None:
        if cls._client:
            await cls._client.close()
            cls._client = None
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None
        logger.info("Redis connection closed.")

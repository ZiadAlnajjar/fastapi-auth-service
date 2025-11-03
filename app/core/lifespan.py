import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.domain.services.cache_client import ICacheClient
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.database.async_engine import AsyncEngine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    try:
        async with AsyncEngine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connected successfully")
    except Exception as e:
        logger.critical(f"Failed to connect to database: {e}")
        raise

    cache_client: ICacheClient = RedisClient()
    await cache_client.init()

    yield

    logger.info("Cleaning up...")

    await AsyncEngine.dispose()
    logger.info("Database connection closed")

    await cache_client.close()

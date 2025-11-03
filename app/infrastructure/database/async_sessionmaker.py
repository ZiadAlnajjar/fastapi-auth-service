from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.infrastructure.database.async_engine import AsyncEngine

AsyncSessionMaker: async_sessionmaker = async_sessionmaker(
    bind=AsyncEngine,
    expire_on_commit=False,
    class_=AsyncSession,
)

from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.async_sessionmaker import AsyncSessionMaker
from app.infrastructure.database.events import register_soft_delete_filter

register_soft_delete_filter()


async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with AsyncSessionMaker() as session:
        yield session

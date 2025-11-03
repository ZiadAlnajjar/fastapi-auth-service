from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.is_development(),
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_pre_ping=True,
)

from contextlib import asynccontextmanager

from app.infrastructure.database.session import get_session


@asynccontextmanager
async def session_context():
    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        yield session
    finally:
        await session_gen.aclose()

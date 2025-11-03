from typing import Protocol

from app.domain.services.cache import ICache


class ICacheClient(Protocol):
    @classmethod
    async def init(cls) -> None:
        ...

    @classmethod
    def get_client(cls) -> ICache:
        ...

    @classmethod
    async def close(cls) -> None:
        ...

from datetime import timedelta
from typing import Protocol, Optional


class ICache(Protocol):
    async def set(self, key: str, value: str, ex: Optional[timedelta] = None) -> None:
        ...

    async def get(self, key: str) -> Optional[str]:
        ...

    async def exists(self, key: str) -> bool:
        ...

    async def delete(self, key: str) -> None:
        ...

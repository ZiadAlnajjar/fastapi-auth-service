from typing import Protocol, TypeVar, Optional, Sequence, Any
from app.infrastructure.database.base import Base

T = TypeVar("T", bound=Base)


class IRepository(Protocol[T]):
    async def add(self, obj: T) -> T:
        ...

    async def get(self, id_: str) -> Optional[T]:
        ...

    async def list(self, limit: int, offset: int) -> Sequence[T]:
        ...

    async def find_by(self, **filters: Any) -> Sequence[T]:
        ...

    async def find_one_by(self, **filters: Any) -> Optional[T]:
        ...

    async def update(self, id_: str, **values: Any) -> Optional[T]:
        ...

    async def delete(self, obj: T) -> None:
        ...

    async def exists(self, **filters: Any) -> bool:
        ...

    async def count(self, **filters: Any) -> int:
        ...

    async def commit(self):
        ...

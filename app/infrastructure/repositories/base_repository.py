from typing import TypeVar, Generic, Type, Optional, Sequence, Any

from sqlalchemy import select, update, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.base_repository import IRepository
from app.infrastructure.database.base import Base

T = TypeVar("T", bound=Base)


class SQLAlchemyRepository(IRepository[T], Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T], include_deleted: bool = False):
        self.session = session
        self.model = model
        self.include_deleted = include_deleted

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get(self, id_: str) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, limit: int = 100, offset: int = 0) -> Sequence[T]:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_by(self, **filters: Any) -> Sequence[T]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_one_by(self, **filters: Any) -> Optional[T]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id_: str, **values: Any) -> Optional[T]:
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one_or_none()

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)

    async def exists(self, **filters: Any) -> bool:
        stmt = select(exists().where(*[getattr(self.model, k) == v for k, v in filters.items()]))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def count(self, **filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

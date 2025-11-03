from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.base_repository import SQLAlchemyRepository
from app.modules.auth.domain.entities.user import User
from app.modules.auth.domain.repositories.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository, SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def find_by_public_id(self, public_id: str) -> Optional[User]:
        return await self.find_one_by(public_id=public_id)

    async def find_by_email(self, email: str) -> Optional[User]:
        return await self.find_one_by(email=email)

    async def find_by_username(self, username: str) -> Optional[User]:
        return await self.find_one_by(username=username)

    async def exists_by_email(self, email: str) -> bool:
        return await self.exists(email=email)

    async def exists_by_username(self, username: str) -> bool:
        return await self.exists(username=username)

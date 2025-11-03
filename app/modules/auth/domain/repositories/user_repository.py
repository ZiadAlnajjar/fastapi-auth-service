from typing import Optional

from app.domain.repositories.base_repository import IRepository
from app.modules.auth.domain.entities.user import User


class IUserRepository(IRepository[User]):
    async def find_by_public_id(self, email: str) -> Optional[User]:
        ...

    async def find_by_email(self, email: str) -> Optional[User]:
        ...

    async def find_by_username(self, username: str) -> Optional[User]:
        ...

    async def exists_by_email(self, email: str) -> bool:
        ...

    async def exists_by_username(self, username: str) -> bool:
        ...

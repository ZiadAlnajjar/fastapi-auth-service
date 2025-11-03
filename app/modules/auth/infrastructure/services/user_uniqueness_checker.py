from app.modules.auth.domain.repositories.user_repository import IUserRepository
from app.modules.auth.domain.services.user_uniqueness_checker import IUserUniquenessChecker


class UserUniquenessChecker(IUserUniquenessChecker):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def email_exists(self, email: str):
        return await self.user_repo.exists_by_email(email)

    async def username_exists(self, username: str):
        return await self.user_repo.exists_by_username(username)

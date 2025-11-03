from app.modules.auth.application.commands.register_user.register_user_command import RegisterUserCommand
from app.modules.auth.application.commands.register_user.register_user_mapper import RegisterUserMapper
from app.modules.auth.domain.exceptions.user_already_exists_exception import UserAlreadyExists
from app.modules.auth.domain.repositories.user_repository import IUserRepository
from app.modules.auth.domain.services.user_uniqueness_checker import IUserUniquenessChecker
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class RegisterUserService:
    def __init__(
            self,
            user_repo: IUserRepository,
            user_uniqueness_checker: IUserUniquenessChecker,
            password_hasher: PasswordHasher
    ):
        self.user_repo = user_repo
        self.user_uniqueness_checker = user_uniqueness_checker
        self.password_hasher = password_hasher

    async def execute(self, command: RegisterUserCommand):
        payload = command
        email, username = str(payload.email), payload.username

        if await self.user_uniqueness_checker.email_exists(email):
            raise UserAlreadyExists("email", email)

        if await self.user_uniqueness_checker.username_exists(username):
            raise UserAlreadyExists("username", username)

        hashed_pw = self.password_hasher.hash(payload.password)
        user = RegisterUserMapper.to_entity(payload, hashed_pw)
        await self.user_repo.add(user)
        await self.user_repo.commit()

        return RegisterUserMapper.to_result(user)

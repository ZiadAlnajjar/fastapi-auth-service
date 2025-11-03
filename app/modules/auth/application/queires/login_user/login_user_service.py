from app.core.config import settings
from app.modules.auth.application.queires.login_user.login_user_mapper import LoginUserMapper
from app.modules.auth.application.queires.login_user.login_user_query import LoginUserQuery
from app.modules.auth.application.queires.login_user.login_user_result import LoginUserResult
from app.modules.auth.domain.exceptions.invalid_credentials import InvalidCredentials
from app.modules.auth.domain.repositories.user_repository import IUserRepository
from app.modules.auth.infrastructure.security.jwt_service import JWTService
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class LoginUserService:
    def __init__(self, user_repo: IUserRepository, password_hasher: PasswordHasher, jwt_service: JWTService):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service
        self.token_type_hint = settings.token_type_hint

    async def execute(self, query: LoginUserQuery) -> LoginUserResult:
        user = await self.user_repo.find_by_email(str(query.email))

        if user is None or not self.password_hasher.verify(query.password, user.hashed_password):
            raise InvalidCredentials()

        access_token = self.jwt_service.create_access_token(str(user.public_id))
        refresh_token = self.jwt_service.create_refresh_token(str(user.public_id))

        return LoginUserMapper.to_result(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type_hint=self.token_type_hint,
        )

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services.cache import ICache
from app.domain.services.cache_client import ICacheClient
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.cache.redis_service import RedisService
from app.infrastructure.database.session import get_session
from app.modules.auth.application.commands.logout_user.logout_user_service import LogoutUserService
from app.modules.auth.application.commands.register_user.register_user_service import RegisterUserService
from app.modules.auth.application.queires.login_user.login_user_service import LoginUserService
from app.modules.auth.application.commands.refresh_token.refresh_token_service import RefreshTokenService
from app.modules.auth.domain.repositories.user_repository import IUserRepository
from app.modules.auth.domain.services.token_blacklist_service import ITokenBlacklistService
from app.modules.auth.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.modules.auth.infrastructure.security.jwt_service import JWTService
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher
from app.modules.auth.infrastructure.services.token_blacklist_service import TokenBlacklistService
from app.modules.auth.infrastructure.services.user_uniqueness_checker import UserUniquenessChecker


async def get_user_repository(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyUserRepository(session)


async def get_user_uniqueness_checker(user_repo: IUserRepository = Depends(get_user_repository)):
    return UserUniquenessChecker(user_repo)


async def get_password_hasher():
    return PasswordHasher()


async def get_jwt_service():
    return JWTService()


async def get_cache_client() -> ICacheClient:
    return RedisClient()


async def get_cache(
        cache_client: ICacheClient = Depends(get_cache_client)
) -> ICache:
    return RedisService(cache_client)


async def get_register_user_service(
        user_repo: IUserRepository = Depends(get_user_repository),
        user_uniqueness_checker: UserUniquenessChecker = Depends(get_user_uniqueness_checker),
        password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    return RegisterUserService(
        user_repo,
        user_uniqueness_checker,
        password_hasher,
    )


async def get_token_blacklist_service(
        cache: ICache = Depends(get_cache),
) -> ITokenBlacklistService:
    return TokenBlacklistService(cache)


async def get_login_user_service(
        user_repo: IUserRepository = Depends(get_user_repository),
        password_hasher: PasswordHasher = Depends(get_password_hasher),
        jwt_service: JWTService = Depends(get_jwt_service),
):
    return LoginUserService(
        user_repo,
        password_hasher,
        jwt_service,
    )


async def get_logout_user_service(
        jwt_service: JWTService = Depends(get_jwt_service),
        token_blacklist_service: ITokenBlacklistService = Depends(get_token_blacklist_service),
):
    return LogoutUserService(jwt_service, token_blacklist_service)


async def get_refresh_token_service(
        jwt_service: JWTService = Depends(get_jwt_service),
        token_blacklist_service: ITokenBlacklistService = Depends(get_token_blacklist_service),
):
    return RefreshTokenService(jwt_service, token_blacklist_service)

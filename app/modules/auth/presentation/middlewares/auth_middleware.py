import re

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.di import get_jwt_service, get_token_blacklist_service, get_user_repository, get_cache, get_cache_client
from app.core.session_context import session_context
from app.modules.auth.domain.entities import User
from app.modules.auth.domain.exceptions.invalid_token_sub import InvalidTokenSub
from app.modules.auth.domain.exceptions.revoked_token_exception import RevokedTokenException
from app.modules.auth.domain.repositories.user_repository import IUserRepository
from app.modules.auth.domain.services.token_blacklist_service import ITokenBlacklistService
from app.modules.auth.infrastructure.security.jwt_service import JWTService
from app.modules.auth.presentation.utils.utils import extract_token, is_request_protected


class AuthMiddleware(BaseHTTPMiddleware):
    jwt_service: JWTService
    token_blacklist_service: ITokenBlacklistService
    user_repo: IUserRepository

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        await self._inject_dependencies()

        is_protected = is_request_protected(request)
        is_refresh = bool(re.match(r"/api/v\d+/auth/token", request.url.path))
        is_logout = bool(re.match(r"/api/v\d+/auth/logout", request.url.path))

        if not is_protected:
            return await call_next(request)

        verify_exp = not (is_refresh or is_logout)
        token = extract_token(request, "access")
        user = await self._get_user_from_token(token, verify_exp)

        if await self.token_blacklist_service.is_token_blacklisted(token):
            raise RevokedTokenException()

        request.state.user = user
        request.state.token = token

        return await call_next(request)

    async def _get_user_from_token(self, token: str, verify_exp: bool = True) -> User:
        sub = self.jwt_service.verify(token, {"verify_exp": verify_exp}, "access")
        return await self._find_user_by_public_id(sub)

    async def _find_user_by_public_id(self, user_id):
        user = await self.user_repo.find_by_public_id(user_id)
        if not user:
            raise InvalidTokenSub
        return user

    async def _inject_dependencies(self):
        cache_client = await get_cache_client()
        cache = await get_cache(cache_client)

        self.jwt_service = await get_jwt_service()
        self.token_blacklist_service = await get_token_blacklist_service(cache)

        async with session_context() as session:
            self.user_repo = await get_user_repository(session)

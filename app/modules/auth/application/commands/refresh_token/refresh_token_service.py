from datetime import datetime

from app.modules.auth.application.commands.refresh_token.refresh_token_mapper import RefreshTokenMapper
from app.modules.auth.application.commands.refresh_token.refresh_token_query import RefreshTokenQuery
from app.modules.auth.application.commands.refresh_token.refresh_token_result import RefreshTokenResult
from app.modules.auth.domain.exceptions.token_user_mismatch_exception import TokenUserMismatchException
from app.modules.auth.domain.services.token_blacklist_service import ITokenBlacklistService
from app.modules.auth.infrastructure.security.jwt_service import JWTService


class RefreshTokenService:
    def __init__(self, jwt_service: JWTService, token_blacklist_service: ITokenBlacklistService):
        self.jwt_service = jwt_service
        self.token_blacklist_service = token_blacklist_service

    async def execute(self, query: RefreshTokenQuery) -> RefreshTokenResult:
        user = query.user
        access_token = query.access_token
        refresh_token = query.refresh_token
        refresh_token_sub = self.jwt_service.verify(refresh_token, token_type="refresh")

        if refresh_token_sub != str(user.public_id):
            raise TokenUserMismatchException

        new_access_token = self.jwt_service.create_access_token(str(user.public_id))

        decoded_access_token = self.jwt_service.decode(access_token, {"verify_exp": False})
        access_token_exp = datetime.fromtimestamp(decoded_access_token.get('exp'))
        now = datetime.now()

        if access_token_exp > now:
            await self.token_blacklist_service.blacklist_token(access_token, access_token_exp - now)

        return RefreshTokenMapper.to_result(access_token=new_access_token)

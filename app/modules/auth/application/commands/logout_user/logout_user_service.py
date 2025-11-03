from datetime import datetime

from app.modules.auth.application.commands.logout_user.logout_user_command import LogoutUserCommand
from app.modules.auth.domain.services.token_blacklist_service import ITokenBlacklistService
from app.modules.auth.infrastructure.security.jwt_service import JWTService


class LogoutUserService:
    def __init__(
            self,
            jwt_service: JWTService,
            token_blacklist_service: ITokenBlacklistService,
    ):
        self.jwt_service = jwt_service
        self.token_blacklist_service = token_blacklist_service

    async def execute(self, command: LogoutUserCommand) -> None:
        payload = command
        access_token, refresh_token = payload.access_token, payload.refresh_token
        decode_options = {"verify_exp": False}

        decoded_access_token = self.jwt_service.decode(access_token, decode_options)
        decoded_refresh_token = self.jwt_service.decode(refresh_token, decode_options)

        access_token_exp = datetime.fromtimestamp(decoded_access_token.get('exp'))
        refresh_token_exp = datetime.fromtimestamp(decoded_refresh_token.get('exp'))
        now = datetime.now()

        if access_token_exp > now:
            await self.token_blacklist_service.blacklist_token(access_token, access_token_exp - now)
        if refresh_token_exp > now:
            await self.token_blacklist_service.blacklist_token(refresh_token, refresh_token_exp - now)

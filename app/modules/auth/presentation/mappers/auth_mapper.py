from typing import Optional

from app.modules.auth.application.commands.logout_user.logout_user_command import LogoutUserCommand
from app.modules.auth.application.commands.refresh_token.refresh_token_query import RefreshTokenQuery
from app.modules.auth.application.commands.refresh_token.refresh_token_result import RefreshTokenResult
from app.modules.auth.application.commands.register_user.register_user_command import RegisterUserCommand
from app.modules.auth.application.commands.register_user.register_user_result import RegisterUserResult
from app.modules.auth.application.queires.login_user.login_user_query import LoginUserQuery
from app.modules.auth.application.queires.login_user.login_user_result import LoginUserResult
from app.modules.auth.domain.entities import User
from app.modules.auth.presentation.dtos.login_request import LoginRequest
from app.modules.auth.presentation.dtos.login_response import LoginResponse
from app.modules.auth.presentation.dtos.refresh_token_response import RefreshTokenResponse
from app.modules.auth.presentation.dtos.register_user_request import RegisterUserRequest
from app.modules.auth.presentation.dtos.register_user_response import RegisterUserResponse


class AuthMapper:
    @staticmethod
    def to_login_query(req: LoginRequest) -> LoginUserQuery:
        return LoginUserQuery.model_validate(req)

    @staticmethod
    def to_login_response(res: LoginUserResult) -> LoginResponse:
        return LoginResponse.model_validate(res)

    @staticmethod
    def to_refresh_token_query(user: User, access_token: str, refresh_token: str) -> RefreshTokenQuery:
        return RefreshTokenQuery(user=user, access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def to_refresh_token_response(res: Optional[RefreshTokenResult]) -> Optional[RefreshTokenResponse]:
        if res is None:
            return None

        return RefreshTokenResponse.model_validate(res)

    @staticmethod
    def to_register_user_command(req: RegisterUserRequest) -> RegisterUserCommand:
        return RegisterUserCommand.model_validate(req)

    @staticmethod
    def to_register_user_response(res: RegisterUserResult) -> RegisterUserResponse:
        return RegisterUserResponse.model_validate(res)

    @staticmethod
    def to_logout_command(access_token: str, refresh_token: Optional[str] = None) -> LogoutUserCommand:
        return LogoutUserCommand(access_token=access_token, refresh_token=refresh_token)

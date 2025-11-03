from app.modules.auth.application.queires.login_user.login_user_result import LoginUserResult


class LoginUserMapper:
    @staticmethod
    def to_result(access_token: str, refresh_token: str, token_type_hint: str) -> LoginUserResult:
        return LoginUserResult(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type_hint=token_type_hint,
        )

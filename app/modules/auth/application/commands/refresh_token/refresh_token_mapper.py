from typing import Optional

from app.modules.auth.application.commands.refresh_token.refresh_token_result import RefreshTokenResult


class RefreshTokenMapper:
    @staticmethod
    def to_result(access_token: Optional[str] = None) -> Optional[RefreshTokenResult]:
        if access_token is None:
            return None

        return RefreshTokenResult(access_token=access_token)

from typing import Optional

from fastapi import Response, Request

from app.core.config import settings
from app.modules.auth.infrastructure.http.token_pair_dto import TokenPairDto


class ResponseTokenBuilder:
    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def _should_use_cookie(self) -> bool:
        is_browser = "text/html" in self.request.headers.get("accept", "")
        wants_cookie = self.request.headers.get("X-Auth-Mode") == "cookie"
        return is_browser or wants_cookie

    def build_pair(self, tokens: TokenPairDto) -> Optional[TokenPairDto]:
        if self._should_use_cookie():
            self.build_access_token(tokens.access_token)
            self.build_refresh_token(tokens.refresh_token)
            return None

        return tokens

    def build_access_token(self, access_token: str) -> Optional[str]:
        if self._should_use_cookie():
            self.response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=settings.access_token_expire_seconds,
            )
            return None

        return access_token

    def build_refresh_token(self, refresh_token: str) -> Optional[str]:
        if self._should_use_cookie():
            self.response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=settings.refresh_token_expire_seconds,
            )
            return None

        return refresh_token

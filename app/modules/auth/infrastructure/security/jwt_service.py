from datetime import datetime, timedelta
from typing import Optional, Mapping, Any

from jose import jwt

from app.core.config import settings
from app.modules.auth.domain.exceptions.invalid_token_type_exception import InvalidTokenTypeException


class JWTService:
    def __init__(self):
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm
        self._access_token_expire_seconds = settings.access_token_expire_seconds
        self._refresh_token_expire_seconds = settings.refresh_token_expire_seconds

    def create_access_token(self, subject: str) -> str:
        to_encode = {
            "sub": subject,
            "exp": datetime.now() + timedelta(seconds=self._access_token_expire_seconds),
            "type": "access",
        }
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, subject: str) -> str:
        to_encode = {
            "sub": subject,
            "exp": datetime.now() + timedelta(seconds=self._refresh_token_expire_seconds),
            "type": "refresh",
        }
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def verify(self, token: str, options: Optional[Mapping[str, Any]] = None, token_type: Optional[str] = None) -> str:
        payload = self.decode(token, options)
        self.is_type(payload, token_type)
        return payload.get("sub")

    def decode(self, token: str, options: Optional[Mapping[str, Any]] = None) -> Optional[dict]:
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm], options=options)

    @staticmethod
    def is_type(payload: dict[str, Any], type_name: str, strict: bool = True) -> bool:
        is_match = payload.get("type") == type_name

        if not is_match:
            if strict:
                raise InvalidTokenTypeException
            return False

        return True

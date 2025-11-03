from datetime import timedelta
from typing import Protocol


class ITokenBlacklistService(Protocol):
    async def blacklist_token(self, token: str, expires_in: timedelta) -> None:
        ...

    async def is_token_blacklisted(self, token: str) -> bool:
        ...

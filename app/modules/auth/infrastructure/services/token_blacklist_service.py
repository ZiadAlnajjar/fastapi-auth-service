from datetime import timedelta

from app.domain.services.cache import ICache
from app.modules.auth.domain.services.token_blacklist_service import ITokenBlacklistService


class TokenBlacklistService(ITokenBlacklistService):
    def __init__(self, cache: ICache):
        self.cache = cache

    async def blacklist_token(self, token: str, expires_in: timedelta):
        await self.cache.set(token, "blacklisted", expires_in)

    async def is_token_blacklisted(self, token: str) -> bool:
        return await self.cache.exists(token)

from typing import Protocol


class IUserUniquenessChecker(Protocol):
    async def email_exists(self, email: str) -> bool:
        ...

    async def username_exists(self, username: str) -> bool:
        ...

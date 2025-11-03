from typing import Protocol

from starlette.requests import Request

from app.modules.auth.domain.entities import User


class AuthenticatedState(Protocol):
    user: User
    token: str


class AuthenticatedRequest(Request):
    state: AuthenticatedState

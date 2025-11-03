from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.routing import Match, BaseRoute

from app.core.config import settings
from app.modules.auth.domain.exceptions.token_exception import TokenException


def _validate_auth_header(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith(f"{settings.token_type_hint} "):
        return None

    return auth_header


def _validate_refresh_header(request: Request) -> str | None:
    refresh_header = request.headers.get("X-Refresh-Token")

    if not refresh_header:
        return None

    return refresh_header


def extract_token(request: Request, token_type: str = "access", strict: bool = True):
    token = request.cookies.get(f"{token_type}_token")

    if token:
        return token

    is_access = token_type == "access"
    is_refresh = token_type == "refresh"

    if is_access:
        auth_header = _validate_auth_header(request)

        if auth_header:
            token = auth_header.split(" ")[1]

    if is_refresh:
        refresh_header = _validate_refresh_header(request)
        token = refresh_header

    if not token:
        if strict:
            raise TokenException()

        return None

    return token


def tag_protected_routes(app: FastAPI, attr_name: str = "is_protected") -> None:
    """
    Iterate over app.routes and copy `func.is_protected` to the route object.

    Example:
        def protected(func):
            func.is_protected = True
            return func

        @router.get("/secret")
        @protected
        async def secret(): ...
    """
    for route in app.routes:
        endpoint = getattr(route, "endpoint", None)
        flag = getattr(endpoint, attr_name, False)
        setattr(route, attr_name, flag)


def find_matching_route(app: FastAPI, request: Request) -> Optional[BaseRoute]:
    """
    Works before routing resolution
    """
    for route in app.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return route
    return None


def is_request_protected(request: Request) -> bool:
    route = find_matching_route(request.app, request)
    return getattr(route, "is_protected", False) if route else False

from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Cookie, Header
from starlette import status
from starlette.responses import Response

from app.core.di import get_register_user_service, get_login_user_service, get_refresh_token_service, \
    get_logout_user_service
from app.modules.auth.application.commands.logout_user.logout_user_service import LogoutUserService
from app.modules.auth.application.commands.register_user.register_user_service import RegisterUserService
from app.modules.auth.application.queires.login_user.login_user_service import LoginUserService
from app.modules.auth.application.commands.refresh_token.refresh_token_service import RefreshTokenService
from app.modules.auth.infrastructure.http.response_token_builder import ResponseTokenBuilder
from app.modules.auth.infrastructure.http.token_pair_dto import TokenPairDto
from app.modules.auth.presentation.decorators.protected_decorator import protected
from app.modules.auth.presentation.decorators.public_decorator import public
from app.modules.auth.presentation.dtos.common_headers import CommonHeaders
from app.modules.auth.presentation.dtos.cookies import Cookies
from app.modules.auth.presentation.dtos.login_request import LoginRequest
from app.modules.auth.presentation.dtos.login_response import LoginResponse
from app.modules.auth.presentation.dtos.refresh_token_response import RefreshTokenResponse
from app.modules.auth.presentation.dtos.register_user_request import RegisterUserRequest
from app.modules.auth.presentation.dtos.user_response import UserResponse
from app.modules.auth.presentation.mappers.auth_mapper import AuthMapper
from app.modules.auth.presentation.types.requests.authenticated_request import AuthenticatedRequest
from app.modules.auth.presentation.utils.utils import extract_token

router = APIRouter(prefix="/v1/auth", tags=["Auth (v1)"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@public
async def register_user(
        body: RegisterUserRequest,
        register_user_service: RegisterUserService = Depends(get_register_user_service),
):
    payload = AuthMapper.to_register_user_command(body)
    user = await register_user_service.execute(payload)
    return AuthMapper.to_register_user_response(user)


@router.post("/login", response_model=Optional[LoginResponse])
@public
async def login_user(
        request: AuthenticatedRequest,
        response: Response,
        body: LoginRequest,
        login_user_service: LoginUserService = Depends(get_login_user_service),
):
    payload = AuthMapper.to_login_query(body)
    tokens = await login_user_service.execute(payload)

    token_builder = ResponseTokenBuilder(request=request, response=response)
    token_response = token_builder.build_pair(TokenPairDto.model_validate(tokens))

    if token_response is not None:
        return AuthMapper.to_login_response(tokens)

    return None


@router.post("/token", response_model=Optional[RefreshTokenResponse])
@protected
async def token(
        request: AuthenticatedRequest,
        response: Response,
        headers: Annotated[CommonHeaders, Header()] = None,
        cookies: Annotated[Cookies, Cookie()] = None,
        refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
):
    user = request.state.user
    access_token = request.state.token
    refresh_token = extract_token(request, "refresh")
    payload = AuthMapper.to_refresh_token_query(user, access_token, refresh_token)
    new_access_token = await refresh_token_service.execute(payload)

    response_token_builder = ResponseTokenBuilder(request=request, response=response)
    token_response = response_token_builder.build_access_token(new_access_token.access_token)

    if token_response is not None:
        return AuthMapper.to_refresh_token_response(new_access_token)

    return None


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@protected
async def logout_user(
        request: AuthenticatedRequest,
        response: Response,
        headers: Annotated[CommonHeaders, Header()] = None,
        cookies: Annotated[Cookies, Cookie()] = None,
        logout_user_service: LogoutUserService = Depends(get_logout_user_service),
):
    access_token = request.state.token
    refresh_token = extract_token(request, "refresh")

    payload = AuthMapper.to_logout_command(access_token, refresh_token)
    await logout_user_service.execute(payload)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return

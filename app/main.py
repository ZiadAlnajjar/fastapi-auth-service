import logging

from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.openapi import custom_openapi
from app.modules.auth.presentation.middlewares.auth_middleware import AuthMiddleware
from app.modules.auth.presentation.utils.utils import tag_protected_routes
from app.presentation import create_router
from app.presentation.middlewares.error_handler_middleware import ErrorHandlerMiddleware

logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    builder = FastAPI(title="Auth API", lifespan=lifespan)

    builder.add_middleware(AuthMiddleware)

    builder.add_middleware(ErrorHandlerMiddleware)

    builder.include_router(create_router(), prefix="/api")

    tag_protected_routes(builder)

    custom_openapi(builder)

    return builder


app = create_app()

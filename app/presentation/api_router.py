from fastapi import APIRouter

from app.modules.auth.presentation.decorators.public_decorator import public
from app.modules.auth.presentation.routes.auth_route import router as auth_router


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth_router)

    @router.get("/health", tags=["System"])
    @public
    async def heath_check():
        return {"status": "ok"}

    return router

from fastapi import APIRouter


def authenticated_router(router: APIRouter):
    for route in router.routes:
        for method in route.methods:
            setattr(route.endpoint, "is_public", False)
    return router

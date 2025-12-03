from fastapi import APIRouter

from app.api import health


def get_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health.router, tags=["health"])
    return router

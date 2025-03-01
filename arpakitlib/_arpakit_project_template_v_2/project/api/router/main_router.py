from fastapi import APIRouter

from project.api.router.v1.main_router import main_v1_api_router

main_api_router = APIRouter()

main_api_router.include_router(
    prefix="/v1",
    router=main_v1_api_router,
)

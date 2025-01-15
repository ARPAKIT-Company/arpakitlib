from fastapi import APIRouter

from src.api.router.v1.main_router import main_v1_api_router

main_api_router = APIRouter()

# API Error Info

main_api_router.include_router(
    router=main_v1_api_router,
    prefix="/api/v1"
)

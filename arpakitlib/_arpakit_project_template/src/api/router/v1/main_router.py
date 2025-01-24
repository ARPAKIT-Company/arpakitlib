from fastapi import APIRouter

from src.api.router.v1 import get_api_error_info

main_v1_api_router = APIRouter()

# API Error Info

main_v1_api_router.include_router(
    router=get_api_error_info.api_router,
    prefix="/get_api_error_info",
    tags=["API Error Info"]
)

# ...

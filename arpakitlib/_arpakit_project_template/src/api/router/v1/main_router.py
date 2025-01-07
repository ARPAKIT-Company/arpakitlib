from fastapi import APIRouter

from src.api.router.v1 import get_api_error_info

api_v1_main_router = APIRouter()

api_v1_main_router.include_router(get_api_error_info.api_router)

from fastapi import APIRouter

from project.api.router.client import get_errors_info

main_client_api_router = APIRouter()

main_client_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info"
)

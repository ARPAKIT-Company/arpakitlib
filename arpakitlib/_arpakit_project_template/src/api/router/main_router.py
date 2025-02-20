from fastapi import APIRouter

from src.api.router import global_healthcheck
from src.api.router.v1.main_router import main_v1_api_router

main_api_router = APIRouter()


# Global healthcheck


main_api_router.include_router(
    router=global_healthcheck.api_router,
    tags=["Global healthcheck"]
)


# V1 API Router


main_api_router.include_router(
    router=main_v1_api_router,
    prefix="/api/v1"
)

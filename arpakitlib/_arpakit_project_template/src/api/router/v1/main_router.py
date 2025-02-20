from fastapi import APIRouter

from src.api.router.v1 import healthcheck, raise_fake_error

main_v1_api_router = APIRouter()

# healthcheck

main_v1_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck",
    tags=["Healthcheck"]
)

# raise fake error

main_v1_api_router.include_router(
    router=raise_fake_error.api_router,
    prefix="/raise_fake_error",
    tags=["raise_fake_error"]
)

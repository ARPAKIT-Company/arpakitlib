from fastapi import APIRouter

from project.api.router.general import healthcheck

main_general_api_router = APIRouter()

main_general_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck"
)

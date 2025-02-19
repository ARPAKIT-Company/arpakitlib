from fastapi import APIRouter

from src.api.router.v1 import get_info_about_errors, healthcheck, arpakitlib_

main_v1_api_router = APIRouter()

# Healthcheck

main_v1_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck",
    tags=["Healthcheck"]
)

# arpakitlib

main_v1_api_router.include_router(
    router=arpakitlib_.api_router,
    prefix="/arpakitlib",
    tags=["arpakitlib"]
)

# API Error Info

main_v1_api_router.include_router(
    router=get_info_about_errors.api_router,
    prefix="/get_info_about_errors",
    tags=["Info about errors"]
)

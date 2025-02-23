from fastapi import APIRouter

from src.api.router.v1 import arpakitlib_, healthcheck, raise_fake_error, get_errors_info, check_auth
from src.core.settings import get_cached_settings

main_v1_api_router = APIRouter()

# arpakitlib_

main_v1_api_router.include_router(
    router=arpakitlib_.api_router,
    prefix="/arpakitlib",
    tags=["arpakitlib"]
)

# Healthcheck

main_v1_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck",
    tags=["Healthcheck"]
)

# Get errors info

main_v1_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info",
    tags=["Errors info"]
)

# Check auth

if get_cached_settings().is_mode_type_not_prod:
    main_v1_api_router.include_router(
        router=check_auth.api_router,
        prefix="/check_auth",
        tags=["Check auth"]
    )

# Raise fake error

main_v1_api_router.include_router(
    router=raise_fake_error.api_router,
    prefix="/raise_fake_error",
    tags=["Fake error"]
)

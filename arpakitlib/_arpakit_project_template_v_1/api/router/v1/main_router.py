from fastapi import APIRouter

from api.router.v1 import healthcheck, get_errors_info, now_utc_datetime, clear_log_file, get_log_file
from api.router.v1 import raise_fake_error, check_auth

main_v1_api_router = APIRouter()

# Healthcheck

main_v1_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck",
    tags=["Healthcheck"]
)

# arpakitlib_

main_v1_api_router.include_router(
    router=arpakitlib_.api_router,
    prefix="/arpakitlib",
    tags=["arpakitlib"]
)

# Get errors info

main_v1_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info",
    tags=["Errors info"]
)

# Check auth

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

# Now UTC Datetime

main_v1_api_router.include_router(
    router=now_utc_datetime.api_router,
    prefix="/now_utc_datetime",
    tags=["Now UTC datetime"]
)

# Log file

main_v1_api_router.include_router(
    router=clear_log_file.api_router,
    prefix="/clear_log_file",
    tags=["Log file"]
)
main_v1_api_router.include_router(
    router=get_log_file.api_router,
    prefix="/get_log_file",
    tags=["Log file"]
)

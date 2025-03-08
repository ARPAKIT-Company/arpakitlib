from fastapi import APIRouter

from project.api.router.general import get_errors_info, healthcheck, now_utc_datetime, get_auth_data, \
    get_arpakitlib_project_template_info
from project.core.settings import get_cached_settings

main_general_api_router = APIRouter()

main_general_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck"
)
main_general_api_router.include_router(
    router=get_arpakitlib_project_template_info.api_router,
    prefix="/get_arpakitlib_project_template_info"
)
main_general_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info"
)
main_general_api_router.include_router(
    router=now_utc_datetime.api_router,
    prefix="/now_utc_datetime"
)
if not get_cached_settings().prod_mode:
    main_general_api_router.include_router(
        router=get_auth_data.api_router,
        prefix="/get_auth_data"
    )

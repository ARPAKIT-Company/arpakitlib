from fastapi import APIRouter

from project.api.router.v1 import healthcheck, get_errors_info, now_utc_datetime, clear_log_file, get_log_file, \
    get_arpakitlib_project_template_info, reinit_sqlalchemy_db, check_auth, raise_fake_error

main_v1_api_router = APIRouter()

main_v1_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck",
    tags=["Healthcheck"]
)

main_v1_api_router.include_router(
    router=get_arpakitlib_project_template_info.api_router,
    prefix="/get_arpakitlib_project_template_info",
    tags=["arpakitlib project template info"]
)

main_v1_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info",
    tags=["Errors info"]
)

main_v1_api_router.include_router(
    router=check_auth.api_router,
    prefix="/check_auth",
    tags=["Check auth"]
)

main_v1_api_router.include_router(
    router=raise_fake_error.api_router,
    prefix="/raise_fake_error",
    tags=["Fake error"]
)

main_v1_api_router.include_router(
    router=now_utc_datetime.api_router,
    prefix="/now_utc_datetime",
    tags=["Now UTC datetime"]
)

main_v1_api_router.include_router(
    router=get_log_file.api_router,
    prefix="/get_log_file",
    tags=["Log file"]
)
main_v1_api_router.include_router(
    router=clear_log_file.api_router,
    prefix="/clear_log_file",
    tags=["Log file"]
)

main_v1_api_router.include_router(
    router=reinit_sqlalchemy_db.api_router,
    prefix="/reinit_sqlalchemy_db",
    tags=["Reinit SQLAlchemy db"]
)

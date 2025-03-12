from fastapi import APIRouter

from project.api.router.admin import get_auth_data, get_arpakitlib_project_template_info, raise_fake_error

main_admin_api_router = APIRouter()

main_admin_api_router.include_router(
    router=get_arpakitlib_project_template_info.api_router,
    prefix="/get_arpakitlib_project_template_info"
)

main_admin_api_router.include_router(
    router=get_auth_data.api_router,
    prefix="/get_auth_data"
)

main_admin_api_router.include_router(
    router=raise_fake_error.api_router,
    prefix="/raise_fake_error"
)

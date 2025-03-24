from fastapi import APIRouter

from project.api.router.admin import get_auth_data, get_arpakitlib_project_template_info, raise_fake_error, \
    reinit_sqlalchemy_db, get_story_log, init_sqlalchemy_db, get_sqlalchemy_db_table_name_to_amount, \
    get_operation_allowed_statuses, get_operation, create_operation, get_operation_allowed_types

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

main_admin_api_router.include_router(
    router=reinit_sqlalchemy_db.api_router,
    prefix="/reinit_sqlalchemy_db"
)

main_admin_api_router.include_router(
    router=get_story_log.api_router,
    prefix="/get_story_log"
)

main_admin_api_router.include_router(
    router=init_sqlalchemy_db.api_router,
    prefix="/init_sqlalchemy_db"
)

main_admin_api_router.include_router(
    router=get_sqlalchemy_db_table_name_to_amount.api_router,
    prefix="/get_sqlalchemy_db_table_name_to_amount"
)

main_admin_api_router.include_router(
    router=get_operation_allowed_statuses.api_router,
    prefix="/get_operation_allowed_statuses"
)

main_admin_api_router.include_router(
    router=get_operation_allowed_types.api_router,
    prefix="/get_operation_allowed_types"
)

main_admin_api_router.include_router(
    router=get_operation.api_router,
    prefix="/get_operation"
)

main_admin_api_router.include_router(
    router=create_operation.api_router,
    prefix="/create_operation"
)

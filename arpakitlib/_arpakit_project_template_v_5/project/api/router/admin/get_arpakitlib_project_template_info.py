import fastapi
from fastapi import APIRouter

from project.api.auth import require_user_token_dbm_api_middleware, APIAuthData, \
    api_auth, require_correct_api_key_or_api_key_dbm_api_middleware
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

api_router = APIRouter()


@api_router.get(
    "",
    name="Get arpakitlib project template info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(middlewares=[
            require_correct_api_key_or_api_key_dbm_api_middleware(require_active_api_key_dbm=True),
            require_user_token_dbm_api_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    arpakitlib_project_template_data = get_arpakitlib_project_template_info()
    return RawDataCommonSO(data=arpakitlib_project_template_data)

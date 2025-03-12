import fastapi.requests
from fastapi import APIRouter

from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.auth import APIAuthData, api_auth, require_user_token_dbm_api_middleware, \
    require_correct_api_key_or_api_key_dbm_api_middleware
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    path="",
    name="Get auth data",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
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
    return RawDataCommonSO(data=transfer_data_to_json_str_to_data(api_auth_data.model_dump()))

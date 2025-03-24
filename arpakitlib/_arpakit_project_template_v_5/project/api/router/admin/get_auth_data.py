import fastapi.requests
from fastapi import APIRouter

from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class GetAuthDataRouteSO(BaseRouteSO, RawDataCommonSO):
    pass


api_router = APIRouter()


@api_router.get(
    path="",
    name="Get auth data",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=GetAuthDataRouteSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    return GetAuthDataRouteSO(data=transfer_data_to_json_str_to_data(api_auth_data.model_dump()))

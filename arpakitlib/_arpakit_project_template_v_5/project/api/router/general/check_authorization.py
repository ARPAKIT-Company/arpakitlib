import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.general.api_key import ApiKeyGeneral1SO
from project.api.schema.out.general.user import UserGeneral1SO
from project.api.schema.out.general.user_token import UserTokenGeneral1SO


class CheckAuthorizationGeneralRouteSO(BaseRouteSO):
    is_current_api_key_ok: bool = False
    is_current_user_token_ok: bool = False
    current_api_key: ApiKeyGeneral1SO | None = None
    current_user_token: UserTokenGeneral1SO | None = None
    current_user: UserGeneral1SO | None = None


api_router = APIRouter()


@api_router.get(
    "",
    name="Check authorization",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=CheckAuthorizationGeneralRouteSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize())
):
    return CheckAuthorizationGeneralRouteSO(
        is_current_api_key_ok=api_auth_data.api_key_dbm is not None,
        is_current_user_token_ok=api_auth_data.user_token_dbm is not None,
        current_api_key=ApiKeyGeneral1SO.from_dbm(simple_dbm=api_auth_data.api_key_dbm),
        current_user_token=UserTokenGeneral1SO.from_dbm(
            simple_dbm=api_auth_data.user_token_dbm
        ) if api_auth_data.user_token_dbm is not None else None
        ,
        current_user=UserGeneral1SO.from_dbm(
            simple_dbm=api_auth_data.user_token_dbm.user
        ) if api_auth_data.user_token_dbm is not None else None
    )

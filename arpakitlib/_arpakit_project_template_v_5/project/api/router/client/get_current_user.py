import fastapi.requests
from fastapi import APIRouter

from project.api.auth import APIAuthData, api_auth, require_user_token_dbm_api_middleware, \
    require_correct_api_key_or_api_key_dbm_api_middleware
from project.api.schema.out.client.user import UserClientSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    "",
    name="Get current user",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=UserClientSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(middlewares=[
            require_correct_api_key_or_api_key_dbm_api_middleware(require_active_api_key_dbm=True),
            require_user_token_dbm_api_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.client]
            )
        ]))
):
    return UserClientSO.from_dbm(
        simple_dbm=api_auth_data.user_token_dbm.user
    )

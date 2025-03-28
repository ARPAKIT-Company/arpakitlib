import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.client.user import User1ClientSO
from project.api.schema.out.client.user_token import UserToken1ClientSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM, UserTokenDBM


class _UserToken1ClientSO(UserToken1ClientSO):
    user: User1ClientSO

    @classmethod
    def from_dbm(cls, *, simple_dbm: UserTokenDBM) -> UserToken1ClientSO:
        simple_dict = simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys(),
            kwargs={
                "user": simple_dbm.user.simple_dict(
                    include_columns_and_sd_properties=User1ClientSO.model_fields.keys()
                )
            }
        )
        return cls.model_validate(simple_dict)


api_router = APIRouter()


@api_router.get(
    "",
    name="Get current user token",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=_UserToken1ClientSO | ErrorCommonSO,
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
                require_user_roles=[UserDBM.Roles.client]
            )
        ]))
):
    return _UserToken1ClientSO.from_dbm(
        simple_dbm=api_auth_data.user_token_dbm
    )

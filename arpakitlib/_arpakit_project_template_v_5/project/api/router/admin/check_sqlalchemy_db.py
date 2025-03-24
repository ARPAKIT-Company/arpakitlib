import fastapi
from fastapi import APIRouter

from project.api.authorize import require_api_key_dbm_api_authorize_middleware, APIAuthorizeData, \
    require_user_token_dbm_api_authorize_middleware, api_authorize
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class CheckSQLAlchemyDbRouteSO(BaseRouteSO, RawDataCommonSO):
    pass


api_router = APIRouter()


@api_router.get(
    path="",
    name="Check sqlalchemy db",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=CheckSQLAlchemyDbRouteSO | ErrorCommonSO
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
    get_cached_sqlalchemy_db().is_conn_good()
    return CheckSQLAlchemyDbRouteSO(
        data={"is_conn_good": get_cached_sqlalchemy_db().is_conn_good()}
    )

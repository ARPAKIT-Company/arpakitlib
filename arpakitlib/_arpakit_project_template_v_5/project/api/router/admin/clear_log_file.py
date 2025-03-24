import fastapi
from fastapi import APIRouter

from arpakitlib.ar_logging_util import init_log_file
from project.api.authorize import require_api_key_dbm_api_authorize_middleware, APIAuthorizeData, \
    require_user_token_dbm_api_authorize_middleware, api_authorize
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class ClearLogFileRouteSO(BaseRouteSO, RawDataCommonSO):
    pass


api_router = APIRouter()


@api_router.get(
    path="",
    name="Clear log file",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ClearLogFileRouteSO | ErrorCommonSO
)
def _(
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
    init_log_file(log_filepath=get_cached_settings().log_filepath)
    with open(file=get_cached_settings().log_filepath, mode="w") as f:
        f.write("")
    return ClearLogFileRouteSO()

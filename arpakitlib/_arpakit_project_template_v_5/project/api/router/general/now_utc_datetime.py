import fastapi
from fastapi import APIRouter

from arpakitlib.ar_datetime_util import now_utc_dt
from project.api.authorize import require_api_key_dbm_api_authorize_middleware, APIAuthorizeData, api_authorize
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.datetime_ import DatetimeCommonSO
from project.api.schema.out.common.error import ErrorCommonSO


class NowUTCDatetimeRouteSO(BaseRouteSO, DatetimeCommonSO):
    pass


api_router = APIRouter()


@api_router.get(
    "",
    name="Now UTC datetime",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=NowUTCDatetimeRouteSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            )
        ]))
):
    return NowUTCDatetimeRouteSO.from_datetime(datetime_=now_utc_dt())

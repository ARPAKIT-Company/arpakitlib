import fastapi
import starlette.status
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO, DatetimeCommonSO
from arpakitlib.ar_datetime_util import now_utc_dt

api_router = APIRouter()


@api_router.get(
    "",
    response_model=DatetimeCommonSO | ErrorCommonSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return DatetimeCommonSO.from_datetime(datetime_=now_utc_dt())

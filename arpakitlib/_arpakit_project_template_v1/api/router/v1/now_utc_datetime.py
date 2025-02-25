import fastapi
from fastapi import APIRouter, Depends

from api.schema.common.out import ErrorCommonSO, DatetimeCommonSO
from api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data
from arpakitlib.ar_datetime_util import now_utc_dt

api_router = APIRouter()


@api_router.get(
    "",
    name="Now UTC datetime",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=DatetimeCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    return DatetimeCommonSO.from_datetime(datetime_=now_utc_dt())

import fastapi
import starlette
from fastapi import APIRouter, Depends
from starlette import status

from src.api.schema.common.out import ErrorCommonSO
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data

api_router = APIRouter()


@api_router.get(
    "",
    response_model=ErrorCommonSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    raise Exception("fake_error")

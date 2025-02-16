import fastapi
import starlette
from fastapi import APIRouter, Depends
from starlette import status

from arpakitlib.ar_fastapi_util import ErrorSO, get_transmitted_api_data
from src.api.schema.v1.out import HealthcheckSO
from src.api.transmitted_api_data import TransmittedAPIData

api_router = APIRouter()


@api_router.get(
    "/healthcheck",
    response_model=HealthcheckSO | ErrorSO,
    status_code=starlette.status.HTTP_200_OK,
    tags=["Healthcheck"]
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    return HealthcheckSO(is_ok=True)

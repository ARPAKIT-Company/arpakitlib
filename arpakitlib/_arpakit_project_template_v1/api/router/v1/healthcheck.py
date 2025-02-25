import fastapi
from fastapi import APIRouter, Depends

from api.schema.common.out import ErrorCommonSO
from api.schema.v1.out import HealthcheckV1SO
from api.transmitted_api_data import get_transmitted_api_data, TransmittedAPIData

api_router = APIRouter()


@api_router.get(
    "",
    name="Healthcheck",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=HealthcheckV1SO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    return HealthcheckV1SO(is_ok=True)

import fastapi
import starlette.status
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO
from api.schema.v1.out import HealthcheckV1SO

api_router = APIRouter()


@api_router.get(
    "",
    response_model=HealthcheckV1SO | ErrorCommonSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return HealthcheckV1SO(is_ok=True)

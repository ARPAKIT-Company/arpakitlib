import fastapi
import starlette.status
from fastapi import APIRouter

from src.api.schema.common.out import HealthcheckCommonSO, ErrorCommonSO

api_router = APIRouter()


@api_router.get(
    "/healthcheck",
    response_model=HealthcheckCommonSO | ErrorCommonSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return HealthcheckCommonSO(is_ok=True)

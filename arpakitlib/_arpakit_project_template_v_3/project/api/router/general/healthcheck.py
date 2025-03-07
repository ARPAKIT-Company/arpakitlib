import fastapi
from fastapi import APIRouter

from project.api.schema.common.out.schema import ErrorCommonSO
from project.api.schema.general.out.schema import HealthcheckGeneralSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Healthcheck",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=HealthcheckGeneralSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response
):
    return HealthcheckGeneralSO(is_ok=True)

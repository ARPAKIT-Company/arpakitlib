import datetime as dt

import fastapi
from fastapi import APIRouter

from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.core.util import now_local_dt


class HealthcheckRouteSO(BaseRouteSO):
    is_ok: bool = True
    datetime: dt.datetime


api_router = APIRouter()


@api_router.get(
    "",
    name="Healthcheck",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=HealthcheckRouteSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response
):
    return HealthcheckRouteSO(is_ok=True, datetime=now_local_dt())

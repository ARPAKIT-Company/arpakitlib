import fastapi
import starlette.status
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get(
    "/healthcheck",
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return {"is_ok": True}
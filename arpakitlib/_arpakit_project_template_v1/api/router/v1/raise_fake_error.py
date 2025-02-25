import fastapi
import starlette
from fastapi import APIRouter
from starlette import status

from api.schema.common.out import ErrorCommonSO

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
):
    raise Exception("fake_error")

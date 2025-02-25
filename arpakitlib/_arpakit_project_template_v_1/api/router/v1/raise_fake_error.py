import fastapi
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Raise fake error",
    response_model=ErrorCommonSO,
    status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    raise Exception("fake_error")

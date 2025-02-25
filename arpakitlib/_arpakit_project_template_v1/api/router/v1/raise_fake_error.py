import fastapi
from fastapi import APIRouter, Depends

from api.schema.common.out import ErrorCommonSO
from api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data

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
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    raise Exception("fake_error")

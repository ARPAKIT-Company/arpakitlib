import fastapi.requests
from fastapi import APIRouter
from starlette import status

from api.const import APIErrorCodes, APIErrorSpecificationCodes
from api.schema.common.out import ErrorCommonSO
from api.schema.v1.out import ErrorsInfoV1SO

api_router = APIRouter()


@api_router.get(
    "",
    response_model=ErrorsInfoV1SO | ErrorCommonSO,
    status_code=status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return ErrorsInfoV1SO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

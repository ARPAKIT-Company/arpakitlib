import fastapi.requests
from fastapi import APIRouter
from starlette import status

from api.const import APIErrorCodes, APIErrorSpecificationCodes
from api.schema.common.out import ErrorCommonSO, ErrorsInfoCommonSO

api_router = APIRouter()


@api_router.get(
    "",
    response_model=ErrorsInfoCommonSO | ErrorCommonSO,
    status_code=status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    return ErrorsInfoCommonSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

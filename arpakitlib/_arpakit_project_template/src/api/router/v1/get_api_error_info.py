import fastapi.requests
from fastapi import APIRouter
from starlette import status

from arpakitlib.ar_fastapi_util import ErrorSO
from src.api.const import APIErrorCodes, APIErrorSpecificationCodes
from src.api.schema.v1.out import APIErrorInfoSO

api_router = APIRouter()


@api_router.get(
    "/",
    response_model=APIErrorInfoSO | ErrorSO,
    status_code=status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response
):
    return APIErrorInfoSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

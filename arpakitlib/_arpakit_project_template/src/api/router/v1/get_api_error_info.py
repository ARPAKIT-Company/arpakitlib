import fastapi.requests
from fastapi import APIRouter, Depends
from starlette import status

from arpakitlib.ar_fastapi_util import ErrorSO, get_transmitted_api_data
from src.api.const import APIErrorCodes, APIErrorSpecificationCodes
from src.api.schema.v1.out import APIErrorInfoSO
from src.api.transmitted_api_data import TransmittedAPIData

api_router = APIRouter()


@api_router.get(
    "",
    name="Get API Error info",
    response_model=APIErrorInfoSO | ErrorSO,
    status_code=status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    return APIErrorInfoSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

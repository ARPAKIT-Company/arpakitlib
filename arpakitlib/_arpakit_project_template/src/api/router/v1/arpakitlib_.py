import fastapi
import starlette.status
from fastapi import APIRouter, Depends

from arpakitlib.ar_fastapi_util import ErrorSO, get_transmitted_api_data
from src.api.schema.v1.out import ARPAKITLIBInfoSO
from src.api.transmitted_api_data import TransmittedAPIData

api_router = APIRouter()


@api_router.get(
    "/arpakitlib",
    response_model=ARPAKITLIBInfoSO | ErrorSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    return ARPAKITLIBInfoSO(arpakitlib=True)

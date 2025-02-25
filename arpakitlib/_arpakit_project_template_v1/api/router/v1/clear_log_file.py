import fastapi
from fastapi import APIRouter, Depends

from api.schema.common.out import RawDataCommonSO, ErrorCommonSO
from api.transmitted_api_data import get_transmitted_api_data, TransmittedAPIData
from arpakitlib.ar_logging_util import init_log_file

api_router = APIRouter()


@api_router.get(
    path="",
    name="Clear log file",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    init_log_file(log_filepath=transmitted_api_data.settings.log_filepath)
    with open(file=transmitted_api_data.settings.log_filepath, mode="w") as f:
        f.write("")
    return RawDataCommonSO(data={"log_file_was_cleared": True})

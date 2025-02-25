import fastapi
from fastapi import APIRouter

from api.schema.common.out import RawDataCommonSO, ErrorCommonSO
from arpakitlib.ar_logging_util import init_log_file
from core.settings import get_cached_settings

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
):
    init_log_file(log_filepath=get_cached_settings().log_filepath)
    with open(file=get_cached_settings().log_filepath, mode="w") as f:
        f.write("")
    return RawDataCommonSO(data={"log_file_was_cleared": True})

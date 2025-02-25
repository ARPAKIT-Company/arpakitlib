import fastapi
from fastapi import APIRouter
from fastapi.responses import FileResponse

from arpakitlib.ar_logging_util import init_log_file
from core.settings import get_cached_settings

api_router = APIRouter()


@api_router.get(
    path="",
    name="Get log file",
    status_code=fastapi.status.HTTP_200_OK,
    response_class=FileResponse
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    init_log_file(log_filepath=get_cached_settings().log_filepath)
    return FileResponse(path=get_cached_settings().log_filepath)

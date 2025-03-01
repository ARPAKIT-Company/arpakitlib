import fastapi
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from arpakitlib.ar_logging_util import init_log_file
from project.api.auth import APIAuthData, api_auth, correct_api_keys_from_settings__validate_api_key_func
from project.core.settings import get_cached_settings

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
        api_auth_data: APIAuthData = Depends(api_auth(
            require_api_key_string=True,
            require_token_string=False,
            validate_api_key_func=correct_api_keys_from_settings__validate_api_key_func(),
            validate_token_func=None,
            require_correct_api_key=True,
            require_correct_token=False,
        ))
):
    init_log_file(log_filepath=get_cached_settings().log_filepath)
    return FileResponse(path=get_cached_settings().log_filepath)

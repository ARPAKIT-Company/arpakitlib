import fastapi
import starlette
from fastapi import APIRouter, Depends
from starlette import status

from src.api.auth import APIAuthData, correct_api_key_from_settings__validate_api_key_func, api_auth
from src.api.schema.v1.out import ErrorSO
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data

api_router = APIRouter()


@api_router.get(
    "/raise_fake_error",
    response_model=ErrorSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data),
        api_auth_data: APIAuthData = Depends(api_auth(
            validate_api_key_func=correct_api_key_from_settings__validate_api_key_func(),
            require_correct_api_key=True,
        )),
):
    raise Exception("raise_fake_error")

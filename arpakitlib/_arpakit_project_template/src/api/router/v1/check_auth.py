import fastapi.requests
from fastapi import APIRouter, Depends
from starlette import status

from src.api.auth import APIAuthData, api_auth, correct_api_key_from_settings__validate_api_key_func, \
    correct_token_from_settings__validate_api_key_func
from src.api.schema.common.out import ErrorCommonSO
from src.api.schema.v1.out import RawDataV1SO
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data

api_router = APIRouter()


@api_router.get(
    "",
    response_model=RawDataV1SO | ErrorCommonSO,
    status_code=status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data),
        api_auth_data: APIAuthData = Depends(api_auth(
            require_api_key_string=False,
            require_token_string=False,
            validate_api_key_func=correct_api_key_from_settings__validate_api_key_func(),
            validate_token_func=correct_token_from_settings__validate_api_key_func(),
            require_correct_api_key=False,
            require_correct_token=False,
        ))
):
    return RawDataV1SO(data=api_auth_data.model_dump())

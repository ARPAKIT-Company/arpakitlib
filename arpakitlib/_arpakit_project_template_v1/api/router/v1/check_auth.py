import fastapi.requests
from fastapi import APIRouter, Depends

from api.auth import APIAuthData, api_auth, correct_api_key_from_settings__validate_api_key_func, \
    correct_token_from_settings__validate_api_key_func
from api.schema.common.out import ErrorCommonSO, RawDataCommonSO
from api.transmitted_api_data import get_transmitted_api_data, TransmittedAPIData

api_router = APIRouter()


@api_router.get(
    path="",
    name="Check auth",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
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
    return RawDataCommonSO(data=api_auth_data.model_dump())

import fastapi.requests
from fastapi import APIRouter, Depends

from project.api.auth import APIAuthData, api_auth, correct_api_keys_from_settings__validate_api_key_func, \
    correct_tokens_from_settings__validate_api_key_func
from project.api.schema.common.out import ErrorCommonSO, RawDataCommonSO

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
        api_auth_data: APIAuthData = Depends(api_auth(
            require_api_key_string=False,
            require_token_string=False,
            validate_api_key_func=correct_api_keys_from_settings__validate_api_key_func(),
            validate_token_func=correct_tokens_from_settings__validate_api_key_func(),
            require_correct_api_key=False,
            require_correct_token=False,
        ))
):
    return RawDataCommonSO(data=api_auth_data.model_dump())

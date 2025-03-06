import fastapi.requests
from fastapi import APIRouter

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from project.api.auth import APIAuthData, api_auth, correct_tokens_from_settings__is_user_token_correct_func, \
    correct_api_keys_from_settings__is_api_key_correct_func
from project.api.schema.common.out import ErrorCommonSO, RawDataCommonSO
from project.core.settings import ModeTypes

api_router = APIRouter()


@api_router.get(
    path="",
    name="Get auth data",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(
            validate_api_key_func=correct_api_keys_from_settings__is_api_key_correct_func(),
            validate_user_token_func=correct_tokens_from_settings__is_user_token_correct_func(),
            require_correct_api_key=False,
            require_correct_user_token=False,
            require_not_mode_type=ModeTypes.prod
        ))
):
    return RawDataCommonSO(data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump()))

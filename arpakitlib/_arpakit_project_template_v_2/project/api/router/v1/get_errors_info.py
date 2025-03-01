import fastapi.requests
from fastapi import APIRouter, Depends

from project.api.auth import APIAuthData, api_auth, correct_api_keys_from_settings__validate_api_key_func
from project.api.const import APIErrorCodes, APIErrorSpecificationCodes
from project.api.schema.common.out import ErrorCommonSO, ErrorsInfoCommonSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Get errors info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ErrorsInfoCommonSO | ErrorCommonSO,
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
    return ErrorsInfoCommonSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

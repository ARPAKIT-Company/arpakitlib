import fastapi.requests
from fastapi import APIRouter, Depends
from starlette import status

from src.api.auth import APIAuthData, api_auth, correct_api_key_from_settings__validate_api_key_func
from src.api.const import APIErrorCodes, APIErrorSpecificationCodes
from src.api.schema.common.out import ErrorsInfoCommonSO, ErrorCommonSO
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data

api_router = APIRouter()


@api_router.get(
    "",
    response_model=ErrorsInfoCommonSO | ErrorCommonSO,
    status_code=status.HTTP_200_OK
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
    return InfoAboutErrorsSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

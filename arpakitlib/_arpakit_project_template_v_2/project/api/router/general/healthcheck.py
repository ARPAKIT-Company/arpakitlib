import fastapi
from fastapi import APIRouter

from project.api.auth import APIAuthData, api_auth, correct_api_keys_from_settings__is_api_key_correct_func
from project.api.schema.common.out import ErrorCommonSO
from project.api.schema.general.out import HealthcheckGeneralSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Healthcheck",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=HealthcheckGeneralSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(
            validate_api_key_func=correct_api_keys_from_settings__is_api_key_correct_func(),
            require_correct_api_key=True,
        ))
):
    return HealthcheckGeneralSO(is_ok=True)

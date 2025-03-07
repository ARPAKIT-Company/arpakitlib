import fastapi
from fastapi import APIRouter

from project.api.auth import APIAuthData, correct_api_keys_from_settings__is_api_key_correct_func, api_auth
from project.api.schema.common.out.schema import RawDataCommonSO, ErrorCommonSO
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

api_router = APIRouter()


@api_router.get(
    "",
    name="Get arpakitlib project template info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO
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
    arpakitlib_project_template_data = get_arpakitlib_project_template_info()
    return RawDataCommonSO(data=arpakitlib_project_template_data)

import fastapi
from fastapi import APIRouter

from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.api.schema.out.general.error import ErrorGeneralSO
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

api_router = APIRouter()


@api_router.get(
    "",
    name="Get arpakitlib project template info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorGeneralSO
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response
):
    arpakitlib_project_template_data = get_arpakitlib_project_template_info()
    return RawDataCommonSO(data=arpakitlib_project_template_data)

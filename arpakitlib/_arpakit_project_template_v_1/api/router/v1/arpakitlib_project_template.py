import fastapi
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO, RawDataCommonSO
from util.read_arpakitlib_project_template_file import read_arpakitlib_project_template_file

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
):
    arpakitlib_project_template_data = read_arpakitlib_project_template_file()
    return RawDataCommonSO(data=arpakitlib_project_template_data)

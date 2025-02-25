import fastapi
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO
from api.schema.v1.out import ARPAKITLIBInfoV1SO
from util.read_arpakitlib_project_template_file import read_arpakitlib_project_template_file

api_router = APIRouter()


@api_router.get(
    "",
    name="Get arpakitlib info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ARPAKITLIBInfoV1SO | ErrorCommonSO
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
):
    arpakitlib_project_template_data = read_arpakitlib_project_template_file()
    return ARPAKITLIBInfoV1SO(
        arpakitlib=True,
        arpakitlib_project_template_version=arpakitlib_project_template_data.get(
            "arpakitlib_project_template_version"
        ),
        data=arpakitlib_project_template_data
    )

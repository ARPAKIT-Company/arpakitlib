import fastapi
import starlette.status
from fastapi import APIRouter, Depends

from src.api.schema.common.out import ARPAKITLIBInfoCommonSO, ErrorCommonSO
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data
from src.util.read_arpakitlib_project_template import read_arpakitlib_project_template

api_router = APIRouter()


@api_router.get(
    "/arpakitlib",
    response_model=ARPAKITLIBInfoCommonSO | ErrorCommonSO,
    status_code=starlette.status.HTTP_200_OK
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
):
    arpakitlib_project_template_data = read_arpakitlib_project_template()
    return ARPAKITLIBInfoCommonSO(
        arpakitlib=True,
        arpakitlib_project_template_version=arpakitlib_project_template_data["arpakitlib_project_template_version"],
        data=arpakitlib_project_template_data
    )

import fastapi.requests
from fastapi import APIRouter

from project.api.const import APIErrorCodes, APIErrorSpecificationCodes
from project.api.schema.common.out.schema import ErrorCommonSO
from project.api.schema.general.out.schema import ErrorsInfoGeneralSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Get errors info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ErrorsInfoGeneralSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response
):
    return ErrorsInfoGeneralSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

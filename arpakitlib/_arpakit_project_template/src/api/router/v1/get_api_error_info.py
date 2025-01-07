from fastapi import APIRouter

from src.api.const import APIErrorCodes, APIErrorSpecificationCodes
from src.api.schema.v1.out import APIErrorInfoSO

api_router = APIRouter()


@api_router.get("/", response_model=APIErrorInfoSO)
async def _():
    return APIErrorInfoSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )

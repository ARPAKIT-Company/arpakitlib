import fastapi.requests
from fastapi import APIRouter
from project.api.schema.out.common.error import ErrorCommonSO

from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.auth import APIAuthData, api_auth
from project.api.schema.out.common.raw_data import RawDataCommonSO

api_router = APIRouter()


@api_router.get(
    path="",
    name="Get auth data",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(
            require_not_prod_mode=True,
            try_find_api_key_dbm_from_sqlalchemy_db=True,
            try_find_user_token_dbm_from_sqlalchemy_db=True,
            require_api_key_dbm_from_sqlalchemy_db=True,
            require_user_token_dbm_from_sqlalchemy_db=True
        ))
):
    return RawDataCommonSO(data=transfer_data_to_json_str_to_data(api_auth_data.model_dump()))

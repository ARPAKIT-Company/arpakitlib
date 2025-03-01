import fastapi
from fastapi import APIRouter

from project.api.auth import APIAuthData, api_auth
from project.api.schema.common.out import ErrorCommonSO, RawDataCommonSO
from project.core.settings import ModeTypes
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db

api_router = APIRouter()


@api_router.get(
    "",
    name="Reinit SQLAlchemy db",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=RawDataCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthData = fastapi.Depends(api_auth(
            require_api_key_string=True,
            require_token_string=False,
            validate_api_key_func=None,
            validate_token_func=None,
            require_correct_api_key=False,
            require_correct_token=False,
            require_not_mode_type=ModeTypes.prod
        ))
):
    get_cached_sqlalchemy_db().reinit()
    return RawDataCommonSO(data={"sqlalchemy_db_was_reinited": True})

import fastapi
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO
from api.schema.v1.out import OperationV1SO
from sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db

api_router = APIRouter()


@api_router.get(
    "",
    name="Get operation",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=OperationV1SO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        filter_id: int | None = None
):
    # TODO
    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        pass

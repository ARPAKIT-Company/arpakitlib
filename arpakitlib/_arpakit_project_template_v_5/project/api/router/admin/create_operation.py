from typing import Any

import fastapi
from fastapi import APIRouter

from arpakitlib.ar_type_util import NotSet, is_set
from project.api.authorize import require_api_key_dbm_api_authorize_middleware, \
    require_user_token_dbm_api_authorize_middleware, APIAuthorizeData, api_authorize
from project.api.schema.common import BaseRouteSO, BaseSI
from project.api.schema.out.admin.operation import OperationAdmin1SO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM, OperationDBM


class CreateOperationAdminSI(BaseSI):
    slug: str | None = NotSet
    type: str
    title: str | None = NotSet
    input_data: dict[str, Any] = NotSet


class CreateOperationRouteSO(BaseRouteSO, OperationAdmin1SO):
    pass


api_router = APIRouter()


@api_router.post(
    "",
    name="Create operation",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=CreateOperationRouteSO | None | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ])),
        create_operation_admin_si: CreateOperationAdminSI = fastapi.Body()
):
    operation_dbm = OperationDBM(
        status=OperationDBM.Statuses.waiting_for_execution
    )

    if is_set(create_operation_admin_si.slug):
        operation_dbm.slug = create_operation_admin_si.slug
    else:
        operation_dbm.slug = None

    if is_set(create_operation_admin_si.type):
        operation_dbm.type = create_operation_admin_si.type

    if is_set(create_operation_admin_si.title):
        operation_dbm.title = create_operation_admin_si.title
    else:
        operation_dbm.title = None

    if is_set(create_operation_admin_si.input_data):
        operation_dbm.input_data = create_operation_admin_si.input_data
    else:
        operation_dbm.input_data = {}

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        async_session.add(operation_dbm)
        await async_session.commit()
        await async_session.refresh(operation_dbm)

    return CreateOperationRouteSO.from_dbm(simple_dbm=operation_dbm)

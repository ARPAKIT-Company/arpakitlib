from typing import Callable

import fastapi
import fastapi.exceptions
import fastapi.responses
import fastapi.security
import sqlalchemy
from fastapi import Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import joinedload

from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.const import APIErrorCodes
from project.api.exception import APIException
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM, UserTokenDBM


class APIAuthData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    # input

    require_api_key_string: bool = False
    require_user_token_string: bool = False

    require_api_key_from_sqlalchemy_db: bool = False
    require_user_token_from_sqlalchemy_db: bool = False

    require_prod_mode: bool = False
    require_not_prod_mode: bool = False

    # output

    api_key_string: str | None = None
    user_token_string: str | None = None

    api_key_dbm: ApiKeyDBM | None = None
    user_token_dbm: UserTokenDBM | None = None

    current_mode_type: str | None = None


def api_auth(
        *,
        require_api_key_string: bool = False,
        require_user_token_string: bool = False,

        require_api_key_from_sqlalchemy_db: bool = False,
        require_user_token_from_sqlalchemy_db: bool = False,

        require_prod_mode: bool | None = None,
) -> Callable:
    if require_api_key_from_sqlalchemy_db:
        require_api_key_string = True

    if require_user_token_from_sqlalchemy_db:
        require_user_token_string = True

    async def async_func(
            *,
            ac: fastapi.security.HTTPAuthorizationCredentials | None = fastapi.Security(
                fastapi.security.HTTPBearer(auto_error=False)
            ),
            api_key_string: str | None = Security(
                APIKeyHeader(name="apikey", auto_error=False)
            ),
            request: fastapi.requests.Request
    ) -> APIAuthData:

        api_auth_data = APIAuthData(
            require_api_key_string=require_api_key_string,
            require_user_token_string=require_user_token_string,

            require_api_key_from_sqlalchemy_db=require_api_key_from_sqlalchemy_db,
            require_user_token_from_sqlalchemy_db=require_user_token_from_sqlalchemy_db,

            require_prod_mode=require_prod_mode
        )

        # parse api_key

        api_auth_data.api_key_string = api_key_string

        if not api_auth_data.api_key_string and "api_key" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["api_key"]
        if not api_auth_data.api_key_string and "api-key" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["api-key"]
        if not api_auth_data.api_key_string and "apikey" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["apikey"]

        if not api_auth_data.api_key_string and "api_key" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["api_key"]
        if not api_auth_data.api_key_string and "api-key" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["api-key"]
        if not api_auth_data.api_key_string and "apikey" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["apikey"]

        if api_auth_data.api_key_string:
            api_auth_data.api_key_string = api_auth_data.api_key_string.strip()
        if not api_auth_data.api_key_string:
            api_auth_data.api_key_string = None

        # parse user token

        api_auth_data.user_token_string = ac.credentials if ac and ac.credentials and ac.credentials.strip() else None

        if not api_auth_data.user_token_string and "token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["token"]

        if not api_auth_data.user_token_string and "user_token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["user_token"]
        if not api_auth_data.user_token_string and "user-token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["user-token"]
        if not api_auth_data.user_token_string and "usertoken" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["usertoken"]

        if not api_auth_data.user_token_string and "token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["token"]

        if not api_auth_data.user_token_string and "user_token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["user_token"]
        if not api_auth_data.user_token_string and "user-token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["user-token"]
        if not api_auth_data.user_token_string and "usertoken" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["usertoken"]

        if api_auth_data.user_token_string:
            api_auth_data.user_token_string = api_auth_data.user_token_string.strip()
        if not api_auth_data.user_token_string:
            api_auth_data.user_token_string = None

        # require_mode_type

        if require_prod_mode is not None:
            if require_prod_mode != get_cached_settings().prod_mode:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
                )

        # require_api_key_string

        if require_api_key_string and not api_auth_data.api_key_string:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

        # set api_key_dbm

        if api_auth_data.api_key_string is not None:
            async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                api_auth_data.api_key_dbm = await async_session.scalar(
                    sqlalchemy.select(ApiKeyDBM).where(ApiKeyDBM.value == api_auth_data.api_key_string)
                )

        # require_api_key_from_sqlalchemy_db

        if api_auth_data.require_api_key_from_sqlalchemy_db:
            if api_auth_data.api_key_dbm is None:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump()),
                )

        # require_user_token_string

        if api_auth_data.require_user_token_string and not api_auth_data.user_token_string:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

        # set user_token_dbm

        if api_auth_data.user_token_string is not None:
            async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                query = sqlalchemy.select(UserTokenDBM).options(joinedload(UserTokenDBM.user)).filter(
                    UserTokenDBM.value == api_auth_data.user_token_string
                )
                api_auth_data.user_token_dbm = (await async_session.execute(query)).scalars().one_or_none()

        # require_user_token_from_sqlalchemy_db

        if api_auth_data.require_user_token_from_sqlalchemy_db:
            if api_auth_data.user_token_dbm is None:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
                )

        return api_auth_data

    return async_func

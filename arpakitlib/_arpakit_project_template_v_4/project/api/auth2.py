from typing import Callable

import fastapi
import fastapi.exceptions
import fastapi.responses
import fastapi.security
from fastapi import Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict

from arpakitlib.ar_func_util import is_async_callable, is_sync_function
from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.const import APIErrorCodes
from project.api.exception import APIException
from project.core.settings import get_cached_settings


class APIAuthData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    api_key_string: str | None = None
    user_token_string: str | None = None

    prod_mode: bool = False


def api_auth(
        *,
        middleware_funcs: list[Callable] | None = None
) -> Callable:
    if middleware_funcs is None:
        middleware_funcs = []

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
            prod_mode=get_cached_settings().prod_mode
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

        # parse user_token

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

        # middleware_funcs

        for middleware_func in middleware_funcs:
            if is_async_callable(middleware_func):
                await middleware_func(
                    api_auth_data=api_auth_data,
                    request=request
                )
            elif is_sync_function(middleware_func):
                middleware_func(
                    api_auth_data=api_auth_data,
                    request=request
                )
            else:
                raise TypeError("unknown middleware_func type")

        return api_auth_data

    return async_func


def require_api_key_string_middleware_func():
    def func(*, api_auth_data: APIAuthData, request: fastapi.requests.Request):
        if api_auth_data.api_key_string is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description="api_key string is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    return func


def require_user_token_string_middleware_func():
    def func(*, api_auth_data: APIAuthData, request: fastapi.requests.Request):
        if api_auth_data.user_token_string is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description="user_token string is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    return func


def require_prod_mode_middleware_func():
    def func(*, api_auth_data: APIAuthData, request: fastapi.requests.Request):
        if not get_cached_settings().prod_mode:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"prod_mode={get_cached_settings().prod_mode}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    return func


def require_not_prod_mode_middleware_func():
    def func(*, api_auth_data: APIAuthData, request: fastapi.requests.Request):
        if get_cached_settings().prod_mode:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"prod_mode={get_cached_settings().prod_mode}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    return func

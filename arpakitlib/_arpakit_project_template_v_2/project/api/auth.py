from typing import Callable

import fastapi
import fastapi.exceptions
import fastapi.responses
import fastapi.security
from fastapi import Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict

from arpakitlib.ar_func_util import is_async_callable, is_sync_function
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from arpakitlib.ar_type_util import raise_for_type
from project.api.const import APIErrorCodes
from project.api.exception import APIException
from project.core.settings import get_cached_settings


class APIAuthData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    require_api_key_string: bool = False
    require_user_token_string: bool = False

    require_correct_api_key: bool = False
    require_correct_user_token: bool = False

    require_mode_type: str | None = None
    require_not_mode_type: str | None = None

    current_mode_type: str | None = None

    user_token_string: str | None = None
    api_key_string: str | None = None

    is_user_token_correct: bool | None = None
    is_api_key_correct: bool | None = None


def api_auth(
        *,
        require_api_key_string: bool = False,
        require_user_token_string: bool = False,

        require_correct_api_key: bool = False,
        require_correct_user_token: bool = False,

        require_mode_type: str | None = None,
        require_not_mode_type: str | None = None,

        validate_api_key_func: Callable | None = None,
        validate_user_token_func: Callable | None = None,
        correct_api_keys: str | list[str] | None = None,
        correct_user_tokens: str | list[str] | None = None,
) -> Callable:
    if isinstance(correct_api_keys, str):
        correct_api_keys = [correct_api_keys]
    if correct_api_keys is not None:
        raise_for_type(correct_api_keys, list)

    if validate_api_key_func is None and correct_api_keys is not None:
        validate_api_key_func = (
            lambda *args, **kwargs_: kwargs_["api_auth_data"].api_key_string in correct_api_keys
        )

    if isinstance(correct_user_tokens, str):
        correct_user_tokens = [correct_user_tokens]
    if correct_user_tokens is not None:
        raise_for_type(correct_user_tokens, list)

    if validate_user_token_func is None and correct_user_tokens is not None:
        validate_user_token_func = (
            lambda *args, **kwargs_: kwargs_["api_auth_data"].user_token_string in correct_user_tokens
        )

    if require_correct_api_key is True:
        require_api_key_string = True

    if require_correct_user_token is True:
        require_user_token_string = True

    async def func(
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
            require_correct_api_key=require_correct_api_key,
            require_correct_user_token=require_correct_user_token,
            require_mode_type=require_mode_type,
            require_not_mode_type=require_not_mode_type,
            current_mode_type=get_cached_settings().mode_type
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

        if require_mode_type is not None:
            if get_cached_settings().mode_type != require_mode_type:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
                )

        # require_not_mode_type

        if require_not_mode_type is not None:
            if get_cached_settings().mode_type == require_not_mode_type:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
                )

        # require_api_key_string

        if require_api_key_string and not api_auth_data.api_key_string:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # require_token_string

        if require_user_token_string and not api_auth_data.user_token_string:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # validate_api_key_func

        if validate_api_key_func is not None:
            if is_async_callable(validate_api_key_func):
                api_auth_data.is_api_key_correct = await validate_api_key_func(
                    api_auth_data=api_auth_data,
                    request=request
                )
            elif is_sync_function(validate_api_key_func):
                api_auth_data.is_api_key_correct = validate_api_key_func()
            else:
                raise TypeError("unknown validate_api_key_func type")

        # validate_token_func

        if validate_user_token_func is not None:
            if is_async_callable(validate_user_token_func):
                api_auth_data.is_user_token_correct = await validate_user_token_func(
                    api_auth_data=api_auth_data,
                    request=request
                )
            elif is_sync_function(validate_user_token_func):
                api_auth_data.is_user_token_correct = validate_user_token_func()
            else:
                raise TypeError("unknown validate_token_func type")

        # require_correct_api_key

        if require_correct_api_key:
            if not api_auth_data.is_api_key_correct:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_api_key_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump()),
                )

        # require_correct_token

        if require_correct_user_token:
            if not api_auth_data.is_user_token_correct:
                raise APIException(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_token_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
                )

        return api_auth_data

    return func


def correct_api_keys_from_settings__is_api_key_correct_func() -> Callable:
    async def async_func(
            *,
            api_auth_data: APIAuthData,
            request: fastapi.requests.Request,
    ):
        if get_cached_settings().api_correct_api_keys is None:
            return False
        if api_auth_data.api_key_string is None:
            return False
        if api_auth_data.api_key_string.strip() not in get_cached_settings().api_correct_api_keys:
            return False
        return True

    return async_func


def correct_tokens_from_settings__is_user_token_correct_func() -> Callable:
    async def async_func(
            *,
            api_auth_data: APIAuthData,
            request: fastapi.requests.Request,
    ):
        if get_cached_settings().api_correct_tokens is None:
            return False
        if api_auth_data.user_token_string is None:
            return False
        if api_auth_data.user_token_string.strip() not in get_cached_settings().api_correct_tokens:
            return False
        return True

    return async_func

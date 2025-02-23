from typing import Callable

import fastapi
import fastapi.exceptions
import fastapi.responses
import fastapi.security
import starlette.exceptions
import starlette.requests
import starlette.requests
import starlette.status
from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict

from arpakitlib.ar_func_util import is_async_object
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from arpakitlib.ar_type_util import raise_for_type, raise_if_none
from src.api.const import APIErrorCodes
from src.api.exception import APIException
from src.api.transmitted_api_data import TransmittedAPIData, get_transmitted_api_data


class APIAuthData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    require_api_key_string: bool = False
    require_token_string: bool = False

    require_correct_api_key: bool = False
    require_correct_token: bool = False

    token_string: str | None = None
    api_key_string: str | None = None

    is_token_correct: bool | None = None
    is_api_key_correct: bool | None = None


def api_auth(
        *,
        require_api_key_string: bool = False,
        require_token_string: bool = False,
        validate_api_key_func: Callable | None = None,
        validate_token_func: Callable | None = None,
        correct_api_keys: str | list[str] | None = None,
        correct_tokens: str | list[str] | None = None,
        require_correct_api_key: bool = False,
        require_correct_token: bool = False,
        **kwargs
) -> Callable:
    if isinstance(correct_api_keys, str):
        correct_api_keys = [correct_api_keys]
    if correct_api_keys is not None:
        raise_for_type(correct_api_keys, list)
        validate_api_key_func = lambda *args, **kwargs_: kwargs_["api_key_string"] in correct_api_keys

    if isinstance(correct_tokens, str):
        correct_tokens = [correct_tokens]
    if correct_tokens is not None:
        raise_for_type(correct_tokens, list)
        validate_token_func = lambda *args, **kwargs_: kwargs_["token_string"] in correct_tokens

    if require_correct_api_key:
        raise_if_none(validate_api_key_func)
        require_api_key_string = True

    if require_correct_token:
        raise_if_none(validate_token_func)
        require_token_string = True

    async def func(
            *,
            ac: fastapi.security.HTTPAuthorizationCredentials | None = fastapi.Security(
                fastapi.security.HTTPBearer(auto_error=False)
            ),
            api_key_string: str | None = Security(
                APIKeyHeader(name="apikey", auto_error=False)
            ),
            request: starlette.requests.Request,
            transmitted_api_data: TransmittedAPIData = Depends(get_transmitted_api_data)
    ) -> APIAuthData:

        api_auth_data = APIAuthData(
            require_api_key_string=require_api_key_string,
            require_token_string=require_token_string,
            require_correct_api_key=require_correct_api_key,
            require_correct_token=require_correct_token
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

        # parse token

        api_auth_data.token_string = ac.credentials if ac and ac.credentials and ac.credentials.strip() else None

        if not api_auth_data.token_string and "token" in request.headers.keys():
            api_auth_data.token_string = request.headers["token"]

        if not api_auth_data.token_string and "user_token" in request.headers.keys():
            api_auth_data.token_string = request.headers["user_token"]
        if not api_auth_data.token_string and "user-token" in request.headers.keys():
            api_auth_data.token_string = request.headers["user-token"]
        if not api_auth_data.token_string and "usertoken" in request.headers.keys():
            api_auth_data.token_string = request.headers["usertoken"]

        if not api_auth_data.token_string and "token" in request.query_params.keys():
            api_auth_data.token_string = request.query_params["token"]

        if not api_auth_data.token_string and "user_token" in request.query_params.keys():
            api_auth_data.token_string = request.query_params["user_token"]
        if not api_auth_data.token_string and "user-token" in request.query_params.keys():
            api_auth_data.token_string = request.query_params["user-token"]
        if not api_auth_data.token_string and "usertoken" in request.query_params.keys():
            api_auth_data.token_string = request.query_params["usertoken"]

        if api_auth_data.token_string:
            api_auth_data.token_string = api_auth_data.token_string.strip()
        if not api_auth_data.token_string:
            api_auth_data.token_string = None

        # require_api_key_string

        if require_api_key_string and not api_auth_data.api_key_string:
            raise APIException(
                status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # require_token_string

        if require_token_string and not api_auth_data.token_string:
            raise APIException(
                status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # validate_api_key_func

        if validate_api_key_func is not None:
            validate_api_key_func_res = validate_api_key_func(
                api_auth_data=api_auth_data,
                transmitted_api_data=transmitted_api_data,
                request=request,
                **kwargs
            )
            if is_async_object(validate_api_key_func_res):
                validate_api_key_func_res = await validate_api_key_func_res
            api_auth_data.is_api_key_correct = validate_api_key_func_res

        # validate_token_func

        if validate_token_func is not None:
            validate_token_func_res = validate_token_func(
                api_auth_data=api_auth_data,
                transmitted_api_data=transmitted_api_data,
                request=request,
                **kwargs
            )
            if is_async_object(validate_token_func_res):
                validate_token_func_res = await validate_token_func_res
            api_auth_data.is_token_correct = validate_token_func_res

        # require_correct_api_key

        if require_correct_api_key:
            if not api_auth_data.is_api_key_correct:
                raise APIException(
                    status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_api_key_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump()),
                )

        # require_correct_token

        if require_correct_token:
            if not api_auth_data.is_token_correct:
                raise APIException(
                    status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_token_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
                )

        return api_auth_data

    return func


def correct_api_key_from_settings__validate_api_key_func() -> Callable:
    async def func(
            *,
            api_auth_data: APIAuthData,
            transmitted_api_data: TransmittedAPIData,
            request: starlette.requests.Request,
            **kwargs
    ):
        if transmitted_api_data.settings.api_correct_api_keys is None:
            return True
        if api_auth_data.api_key_string is None:
            return False
        if api_auth_data.api_key_string.strip() not in transmitted_api_data.settings.api_correct_api_keys:
            return False
        return True

    return func


def correct_token_from_settings__validate_api_key_func() -> Callable:
    async def func(
            *,
            api_auth_data: APIAuthData,
            transmitted_api_data: TransmittedAPIData,
            request: starlette.requests.Request,
            **kwargs
    ):
        if transmitted_api_data.settings.api_correct_tokens is None:
            return True
        if api_auth_data.token_string is None:
            return False
        if api_auth_data.token_string.strip() not in transmitted_api_data.settings.api_correct_tokens:
            return False
        return True

    return func

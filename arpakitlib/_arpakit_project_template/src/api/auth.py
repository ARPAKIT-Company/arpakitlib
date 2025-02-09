# ...
from typing import Callable

import starlette.requests

from arpakitlib.ar_fastapi_util import BaseAPIAuthData
from src.api.transmitted_api_data import TransmittedAPIData


def correct_api_key_from_settings__validate_api_key_func(
        *args, **kwargs
) -> Callable:
    async def func(
            *,
            api_key_string: str | None,
            token_string: str | None,
            base_api_auth_data: BaseAPIAuthData,
            transmitted_api_data: TransmittedAPIData,
            request: starlette.requests.Request,
            **kwargs_
    ):
        if transmitted_api_data.settings.api_correct_api_key is None:
            return True
        if not api_key_string:
            return False
        if api_key_string.strip() != transmitted_api_data.settings.api_correct_api_key.strip():
            return False
        return True

    return func


def correct_token_from_settings__validate_api_key_func(
        *args, **kwargs
) -> Callable:
    async def func(
            *,
            api_key_string: str | None,
            token_string: str | None,
            base_api_auth_data: BaseAPIAuthData,
            transmitted_api_data: TransmittedAPIData,
            request: starlette.requests.Request,
            **kwargs_
    ):
        if transmitted_api_data.settings.api_correct_token is None:
            return True
        if not token_string:
            return False
        if token_string.strip() != transmitted_api_data.settings.api_correct_token.strip():
            return False
        return True

    return func

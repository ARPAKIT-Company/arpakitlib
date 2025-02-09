import fastapi.exceptions
import starlette.exceptions
import starlette.status

from arpakitlib.ar_fastapi_util import create_handle_exception, story_log__api_func_before_in_handle_exception, \
    logging__api_func_before_in_handle_exception
from src.api.const import APIErrorCodes
from src.api.transmitted_api_data import TransmittedAPIData


def create_handle_exception_(*, transmitted_api_data: TransmittedAPIData, **kwargs):
    funcs_before = []

    if transmitted_api_data.settings.api_logging__api_func_before_in_handle_exception:
        funcs_before.append(
            logging__api_func_before_in_handle_exception(
                ignore_api_error_codes=[
                    APIErrorCodes.cannot_authorize,
                    APIErrorCodes.error_in_request,
                    APIErrorCodes.not_found
                ],
                ignore_status_codes=[
                    starlette.status.HTTP_401_UNAUTHORIZED,
                    starlette.status.HTTP_422_UNPROCESSABLE_ENTITY,
                    starlette.status.HTTP_404_NOT_FOUND
                ],
                ignore_exception_types=[
                    fastapi.exceptions.RequestValidationError
                ],
                need_exc_info=False
            )
        )

    if transmitted_api_data.settings.api_story_log__api_func_before_in_handle_exception:
        funcs_before.append(
            story_log__api_func_before_in_handle_exception(
                sqlalchemy_db=transmitted_api_data.sqlalchemy_db,
                ignore_api_error_codes=[
                    APIErrorCodes.cannot_authorize,
                    APIErrorCodes.error_in_request,
                    APIErrorCodes.not_found
                ],
                ignore_status_codes=[
                    starlette.status.HTTP_401_UNAUTHORIZED,
                    starlette.status.HTTP_422_UNPROCESSABLE_ENTITY,
                    starlette.status.HTTP_404_NOT_FOUND
                ],
                ignore_exception_types=[
                    fastapi.exceptions.RequestValidationError
                ],
            )
        )

    async_funcs_after = []

    return create_handle_exception(
        funcs_before=funcs_before,
        async_funcs_after=async_funcs_after
    )

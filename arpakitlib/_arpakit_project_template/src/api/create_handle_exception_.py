import fastapi.exceptions
import starlette.exceptions
import starlette.status

from arpakitlib.ar_fastapi_util import create_handle_exception, story_log_func_before_response, \
    logging_func_before_response
from src.api.const import APIErrorCodes
from src.api.transmitted_api_data import TransmittedAPIData


def create_handle_exception_(*, transmitted_api_data: TransmittedAPIData):
    funcs_before_response = []

    if transmitted_api_data.settings.api_logging_func_before_response:
        funcs_before_response.append(
            logging_func_before_response(
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

    if transmitted_api_data.settings.api_story_log_func_before_response:
        funcs_before_response.append(
            story_log_func_before_response(
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

    async_funcs_after_response = []

    return create_handle_exception(
        funcs_before_response=funcs_before_response,
        async_funcs_after_response=async_funcs_after_response
    )

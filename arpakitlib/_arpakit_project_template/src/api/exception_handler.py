import inspect
import logging
from typing import Any, Callable

import fastapi.exceptions
import fastapi.exceptions
import fastapi.responses
import fastapi.security
import starlette.exceptions
import starlette.exceptions
import starlette.requests
import starlette.status
import starlette.status

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_exception_util import exception_to_traceback_str
from arpakitlib.ar_fastapi_util import create_exception_handler, ErrorSO
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from arpakitlib.ar_type_util import raise_for_type
from src.api.const import APIErrorCodes
from src.api.transmitted_api_data import TransmittedAPIData
from src.sqlalchemy_db.sqlalchemy_model import StoryLogDBM

_logger = logging.getLogger(__name__)


def logging__api_func_before_in_handle_exception(
        *,
        ignore_api_error_codes: list[str] | None = None,
        ignore_status_codes: list[int] | None = None,
        ignore_exception_types: list[type[Exception]] | None = None,
        need_exc_info: bool = False
) -> Callable:
    current_func_name = inspect.currentframe().f_code.co_name

    def func(
            *,
            request: starlette.requests.Request,
            status_code: int,
            error_so: ErrorSO,
            exception: Exception,
            transmitted_kwargs: dict[str, Any],
            **kwargs
    ) -> (ErrorSO, dict[str, Any]):
        transmitted_kwargs[current_func_name] = now_utc_dt()

        if ignore_api_error_codes and error_so.error_code in ignore_api_error_codes:
            return error_so, transmitted_kwargs

        if ignore_status_codes and status_code in ignore_status_codes:
            return error_so, transmitted_kwargs

        if ignore_exception_types and (
                exception in ignore_exception_types or type(exception) in ignore_exception_types
        ):
            return error_so, transmitted_kwargs

        _logger.error(safely_transfer_obj_to_json_str(error_so.model_dump()), exc_info=need_exc_info)

    return func


def story_log__api_func_before_in_handle_exception(
        *,
        sqlalchemy_db: SQLAlchemyDb,
        ignore_api_error_codes: list[str] | None = None,
        ignore_status_codes: list[int] | None = None,
        ignore_exception_types: list[type[Exception]] | None = None
) -> Callable:
    raise_for_type(sqlalchemy_db, SQLAlchemyDb)

    current_func_name = inspect.currentframe().f_code.co_name

    async def async_func(
            *,
            request: starlette.requests.Request,
            status_code: int,
            error_so: ErrorSO,
            exception: Exception,
            transmitted_kwargs: dict[str, Any],
            **kwargs
    ) -> (ErrorSO, dict[str, Any]):
        transmitted_kwargs[current_func_name] = now_utc_dt()

        if ignore_api_error_codes and error_so.error_code in ignore_api_error_codes:
            return error_so, transmitted_kwargs

        if ignore_status_codes and status_code in ignore_status_codes:
            return error_so, transmitted_kwargs

        if ignore_exception_types and (
                exception in ignore_exception_types or type(exception) in ignore_exception_types
        ):
            return error_so, transmitted_kwargs

        async with sqlalchemy_db.new_async_session() as session:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=f"{status_code}, {type(exception)}",
                data={
                    "error_so": error_so.model_dump(),
                    "traceback_str": exception_to_traceback_str(exception=exception)
                }
            )
            session.add(story_log_dbm)
            await session.commit()
            await session.refresh(story_log_dbm)

        error_so.error_data.update({"story_log_long_id": story_log_dbm.long_id})
        transmitted_kwargs["story_log_id"] = story_log_dbm.id

        return error_so, transmitted_kwargs

    return async_func


def create_exception_handler_(*, transmitted_api_data: TransmittedAPIData, **kwargs):
    funcs_before = []
    async_funcs_after = []

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

    return create_exception_handler(
        funcs_before=funcs_before,
        async_funcs_after=async_funcs_after
    )

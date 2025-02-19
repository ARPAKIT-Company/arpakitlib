import asyncio
import inspect
import logging
from contextlib import suppress
from typing import Any, Callable

import fastapi.exceptions
import fastapi.exceptions
import fastapi.responses
import fastapi.security
import starlette.exceptions
import starlette.exceptions
import starlette.requests
import starlette.status

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_exception_util import exception_to_traceback_str
from arpakitlib.ar_func_util import is_async_object, raise_if_not_async_callable
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from arpakitlib.ar_type_util import raise_for_type
from src.api.const import APIErrorCodes
from src.api.exception import APIException
from src.api.response import APIJSONResponse
from src.api.schema.v1.out import ErrorSO
from src.api.transmitted_api_data import TransmittedAPIData
from src.sqlalchemy_db.sqlalchemy_model import StoryLogDBM

_logger = logging.getLogger(__name__)


def create_exception_handler(
        *,
        funcs_before: list[Callable | None] | None = None,
        async_funcs_after: list[Callable | None] | None = None,
        **kwargs
) -> Callable:
    if funcs_before is None:
        funcs_before = []
    funcs_before = [v for v in funcs_before if v is not None]

    if async_funcs_after is None:
        async_funcs_after = []
    async_funcs_after = [v for v in async_funcs_after if v is not None]

    async def func(
            request: starlette.requests.Request,
            exception: Exception
    ) -> APIJSONResponse:
        status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR

        error_so = ErrorSO(
            has_error=True,
            error_code=APIErrorCodes.unknown_error,
            error_data={
                "exception_type": str(type(exception)),
                "exception_str": str(exception),
                "request.method": str(request.method),
                "request.url": str(request.url)
            }
        )

        if isinstance(exception, APIException):
            old_error_data = error_so.error_data
            error_so = exception.error_so
            error_so.error_data = combine_dicts(old_error_data, error_so.error_data)

        elif isinstance(exception, starlette.exceptions.HTTPException):
            status_code = exception.status_code
            if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
                error_so.error_code = APIErrorCodes.cannot_authorize
            elif status_code == starlette.status.HTTP_404_NOT_FOUND:
                error_so.error_code = APIErrorCodes.not_found
            else:
                status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            with suppress(Exception):
                error_so.error_data["exception.detail"] = exception.detail

        elif isinstance(exception, fastapi.exceptions.RequestValidationError):
            status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
            error_so.error_code = APIErrorCodes.error_in_request
            with suppress(Exception):
                error_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}

        else:
            status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            error_so.error_code = APIErrorCodes.unknown_error

        if error_so.error_code is not None:
            error_so.error_code = error_so.error_code.upper().replace(" ", "_").strip()

        if error_so.error_specification_code is not None:
            error_so.error_specification_code = (
                error_so.error_specification_code.upper().replace(" ", "_").strip()
            )

        if error_so.error_code == APIErrorCodes.not_found:
            status_code = starlette.status.HTTP_404_NOT_FOUND

        if error_so.error_code == APIErrorCodes.cannot_authorize:
            status_code = starlette.status.HTTP_401_UNAUTHORIZED

        error_so.error_data["status_code"] = status_code

        # funcs_before

        _transmitted_kwargs = {}
        for func_before in funcs_before:
            _func_data = func_before(
                request=request, status_code=status_code, error_so=error_so, exception=exception,
                transmitted_kwargs=_transmitted_kwargs
            )
            if is_async_object(_func_data):
                _func_data = await _func_data
            if _func_data is not None:
                error_so, _transmitted_kwargs = _func_data[0], _func_data[1]
                raise_for_type(error_so, ErrorSO)
                raise_for_type(_transmitted_kwargs, dict)

        # async_funcs_after

        for async_func_after in async_funcs_after:
            raise_if_not_async_callable(async_func_after)
            _ = asyncio.create_task(async_func_after(
                request=request, status_code=status_code, error_so=error_so, exception=exception
            ))

        return APIJSONResponse(
            content=error_so,
            status_code=status_code
        )

    return func


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

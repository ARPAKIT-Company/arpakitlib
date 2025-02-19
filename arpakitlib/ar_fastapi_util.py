# arpakit

from __future__ import annotations

import asyncio
import logging
import os.path
import pathlib
from contextlib import suppress
from typing import Any, Callable

import fastapi.exceptions
import fastapi.responses
import fastapi.security
import starlette.exceptions
import starlette.requests
import starlette.status
from fastapi import FastAPI, APIRouter, Security, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict
from starlette import status
from starlette.staticfiles import StaticFiles

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_func_util import raise_if_not_async_callable, is_async_object
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from arpakitlib.ar_type_util import raise_for_type, raise_if_none

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

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
            error_code=BaseAPIErrorCodes.unknown_error,
            error_data={
                "exception_type": str(type(exception)),
                "exception_str": str(exception),
                "request.method": str(request.method),
                "request.url": str(request.url),
                "request.headers": str(request.headers),
            }
        )

        if isinstance(exception, APIException):
            old_error_data = error_so.error_data
            error_so = exception.error_so
            error_so.error_data = combine_dicts(old_error_data, error_so.error_data)

        elif isinstance(exception, starlette.exceptions.HTTPException):
            status_code = exception.status_code
            if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
                error_so.error_code = BaseAPIErrorCodes.cannot_authorize
            elif status_code == starlette.status.HTTP_404_NOT_FOUND:
                error_so.error_code = BaseAPIErrorCodes.not_found
            else:
                status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            with suppress(Exception):
                error_so.error_data["exception.detail"] = exception.detail

        elif isinstance(exception, fastapi.exceptions.RequestValidationError):
            status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
            error_so.error_code = BaseAPIErrorCodes.error_in_request
            with suppress(Exception):
                error_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}

        else:
            status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            error_so.error_code = BaseAPIErrorCodes.unknown_error

        if error_so.error_code is not None:
            error_so.error_code = error_so.error_code.upper().replace(" ", "_").strip()

        if error_so.error_specification_code is not None:
            error_so.error_specification_code = (
                error_so.error_specification_code.upper().replace(" ", "_").strip()
            )

        if error_so.error_code == BaseAPIErrorCodes.not_found:
            status_code = status.HTTP_404_NOT_FOUND

        if error_so.error_code == BaseAPIErrorCodes.cannot_authorize:
            status_code = status.HTTP_401_UNAUTHORIZED

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


def add_exception_handler_to_app(*, app: FastAPI, handle_exception: Callable) -> FastAPI:
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=ValueError,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=starlette.exceptions.HTTPException,
        handler=handle_exception
    )
    return app


def add_swagger_to_app(
        *,
        app: FastAPI,
        favicon_url: str | None = None
):
    app.mount(
        "/ar_fastapi_static",
        StaticFiles(directory=os.path.join(str(pathlib.Path(__file__).parent), "ar_fastapi_static")),
        name="ar_fastapi_static"
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title,
            swagger_js_url="/ar_fastapi_static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/ar_fastapi_static/swagger-ui/swagger-ui.css",
            swagger_favicon_url=favicon_url
        )

    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title,
            redoc_js_url="/ar_fastapi_static/redoc/redoc.standalone.js",
            redoc_favicon_url=favicon_url
        )

    return app


def create_fastapi_app(
        *,
        title: str | None = "arpakitlib FastAPI",
        description: str | None = "arpakitlib FastAPI",
        exception_handler: Callable | None = None,
        startup_api_events: list[BaseStartupAPIEvent | None] | None = None,
        shutdown_api_events: list[BaseShutdownAPIEvent | None] | None = None,
        transmitted_api_data: BaseTransmittedAPIData = BaseTransmittedAPIData(),
        main_api_router: APIRouter | None = None,
        contact: dict[str, Any] | None = None,
        media_dirpath: str | None = None,
        static_dirpath: str | None = None,
        **kwargs
):
    _logger.info("start")

    if title is None:
        title = "arpakitlib FastAPI"

    if exception_handler is None:
        exception_handler = create_exception_handler(
            funcs_before=[
                logging__api_func_before_in_handle_exception()
            ]
        )

    if not startup_api_events:
        startup_api_events = [BaseStartupAPIEvent()]
    startup_api_events = [v for v in startup_api_events if v is not None]

    if not shutdown_api_events:
        shutdown_api_events = [BaseShutdownAPIEvent()]
    shutdown_api_events = [v for v in shutdown_api_events if v is not None]

    app = FastAPI(
        title=title,
        description=description,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi",
        on_startup=[api_startup_event.async_on_startup for api_startup_event in startup_api_events],
        on_shutdown=[api_shutdown_event.async_on_shutdown for api_shutdown_event in shutdown_api_events],
        contact=contact,
    )

    if media_dirpath is not None:
        if not os.path.exists(media_dirpath):
            os.makedirs(media_dirpath, exist_ok=True)
        app.mount("/media", StaticFiles(directory=media_dirpath), name="media")

    if static_dirpath is not None:
        if not os.path.exists(static_dirpath):
            os.makedirs(static_dirpath, exist_ok=True)
        app.mount("/static", StaticFiles(directory=static_dirpath), name="static")

    app.state.transmitted_api_data = transmitted_api_data

    add_cors_to_app(app=app)

    add_swagger_to_app(app=app)

    add_exception_handler_to_app(
        app=app,
        handle_exception=exception_handler
    )

    if main_api_router is not None:
        app.include_router(router=main_api_router)

    _logger.info("finish")

    return app


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

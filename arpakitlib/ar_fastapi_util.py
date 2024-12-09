# arpakit

from __future__ import annotations

import asyncio
import logging
import os.path
import pathlib
from datetime import datetime
from typing import Any, Callable

import fastapi.exceptions
import fastapi.responses
import starlette.exceptions
import starlette.requests
import starlette.status
from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from jaraco.context import suppress
from pydantic import BaseModel, ConfigDict
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration import EasyEnumeration
from arpakitlib.ar_json_util import safely_transfer_to_json_str_to_json_obj
from arpakitlib.ar_logging_util import setup_normal_logging

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if not (
                cls.__name__.endswith("SO")
                or cls.__name__.endswith("SI")
                or cls.__name__.endswith("SchemaIn")
                or cls.__name__.endswith("SchemaOut")
        ):
            raise ValueError("APISchema class should ends with SO | SI | SchemaIn | SchemaOut")
        super().__init_subclass__(**kwargs)


class BaseSI(BaseSchema):
    pass


class BaseSO(BaseSchema):
    pass


class SimpleSO(BaseSO):
    id: int
    long_id: str
    creation_dt: datetime


class ErrorSO(BaseSO):
    class APIErrorCodes(EasyEnumeration):
        cannot_authorize = "CANNOT_AUTHORIZE"
        unknown_error = "UNKNOWN_ERROR"
        error_in_request = "ERROR_IN_REQUEST"
        not_found = "NOT_FOUND"

    has_error: bool = True
    error_code: str | None = None
    error_code_specification: str | None = None
    error_description: str | None = None
    error_data: dict[str, Any] = {}


class RawDataSO(BaseSO):
    data: dict[str, Any] = {}


class StoryLogSO(SimpleSO):
    level: str
    title: str | None
    data: dict[str, Any]


class OperationSO(SimpleSO):
    execution_start_dt: datetime | None
    execution_finish_dt: datetime | None
    status: str
    type: str
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]
    duration_total_seconds: float | None


class EasyJSONResponse(fastapi.responses.JSONResponse):
    def __init__(self, *, content: BaseSO, status_code: int = starlette.status.HTTP_200_OK):
        super().__init__(
            content=safely_transfer_to_json_str_to_json_obj(content.model_dump()),
            status_code=status_code
        )


class EasyAPIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = starlette.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = ErrorSO.APIErrorCodes.unknown_error,
            error_code_specification: str | None = None,
            error_description: str | None = None,
            error_data: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_code_specification = error_code_specification
        self.error_description = error_description
        if error_data is None:
            error_data = {}
        self.error_data = error_data

        self.error_so = ErrorSO(
            has_error=True,
            error_code=self.error_code,
            error_specification=self.error_code_specification,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.error_so.model_dump(mode="json")
        )


async def simple_handle_exception(request: starlette.requests.Request, exception: Exception) -> EasyJSONResponse:
    return await from_exception_to_easy_json_response(request=request, exception=exception)


async def from_exception_to_easy_json_response(
        request: starlette.requests.Request, exception: Exception
) -> EasyJSONResponse:
    api_error_so = ErrorSO(
        has_error=True,
        error_code=ErrorSO.APIErrorCodes.unknown_error,
        error_data={
            "exception_type": str(type(exception)),
            "exception_str": str(exception),
            "request.method": str(request.method),
            "request.url": str(request.url),
        }
    )

    status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR

    need_exc_info = True

    if isinstance(exception, EasyAPIException):
        old_error_data = api_error_so.error_data
        api_error_so = exception.error_so
        api_error_so.error_data = combine_dicts(old_error_data, api_error_so.error_data)
        need_exc_info = False

    elif isinstance(exception, starlette.exceptions.HTTPException):
        status_code = exception.status_code
        if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
            api_error_so.error_code = ErrorSO.APIErrorCodes.cannot_authorize
            need_exc_info = False
        elif status_code == starlette.status.HTTP_404_NOT_FOUND:
            api_error_so.error_code = ErrorSO.APIErrorCodes.not_found
            need_exc_info = False
        else:
            status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            need_exc_info = True
        with suppress(Exception):
            api_error_so.error_data["exception.detail"] = exception.detail

    elif isinstance(exception, fastapi.exceptions.RequestValidationError):
        status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
        api_error_so.error_code = ErrorSO.APIErrorCodes.error_in_request
        with suppress(Exception):
            api_error_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}
        need_exc_info = False

    else:
        status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
        api_error_so.error_code = ErrorSO.APIErrorCodes.unknown_error
        _logger.exception(exception)
        need_exc_info = True

    if api_error_so.error_code:
        api_error_so.error_code = api_error_so.error_code.upper().replace(" ", "_").strip()

    if api_error_so.error_code_specification:
        api_error_so.error_code_specification = (
            api_error_so.error_code_specification.upper().replace(" ", "_").strip()
        )

    if need_exc_info:
        _logger.error(str(exception), exc_info=exception)
    else:
        _logger.error(str(exception))

    return EasyJSONResponse(
        content=api_error_so,
        status_code=status_code
    )


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


def add_middleware_cors_to_app(*, app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def add_normalized_swagger_to_app(
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


class BaseStartupAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info("on_startup starts")
        self._logger.info("on_startup ends")


class BaseShutdownAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info("on_shutdown starts")
        self._logger.info("on_shutdown ends")


def simple_api_router_for_testing():
    router = APIRouter(tags=["Testing"])

    @router.get(
        "/healthcheck",
        response_model=RawDataSO | ErrorSO
    )
    async def _():
        return RawDataSO(data={"healthcheck": True})

    @router.get(
        "/raise_fake_exception_1",
        response_model=ErrorSO
    )
    async def _():
        raise fastapi.HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.get(
        "/raise_fake_exception_2",
        response_model=ErrorSO
    )
    async def _():
        raise EasyAPIException(
            error_code="raise_fake_exception_2",
            error_code_specification="raise_fake_exception_2",
            error_description="raise_fake_exception_2"
        )

    @router.get(
        "/raise_fake_exception_3",
        response_model=ErrorSO
    )
    async def _():
        raise Exception("raise_fake_exception_3")

    return router


class BaseTransmittedAPIData(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)


def get_transmitted_api_data(request: starlette.requests.Request) -> BaseTransmittedAPIData:
    return request.app.state.transmitted_api_data


def create_fastapi_app(
        *,
        title: str = "ARPAKITLIB FastAPI",
        description: str | None = "ARPAKITLIB FastAPI",
        log_filepath: str | None = "./story.log",
        handle_exception: Callable | None = simple_handle_exception,
        startup_api_events: list[BaseStartupAPIEvent] | None = None,
        shutdown_api_events: list[BaseStartupAPIEvent] | None = None,
        api_router: APIRouter = simple_api_router_for_testing(),
        transmitted_api_data: BaseTransmittedAPIData = BaseTransmittedAPIData()
):
    setup_normal_logging(log_filepath=log_filepath)

    if not startup_api_events:
        startup_api_events = [BaseStartupAPIEvent()]

    if not shutdown_api_events:
        shutdown_api_events = [BaseShutdownAPIEvent()]

    app = FastAPI(
        title=title,
        description=description,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi",
        on_startup=[api_startup_event.async_on_startup for api_startup_event in startup_api_events],
        on_shutdown=[api_shutdown_event.async_on_shutdown for api_shutdown_event in shutdown_api_events]
    )

    app.state.transmitted_api_data = transmitted_api_data

    add_middleware_cors_to_app(app=app)

    add_normalized_swagger_to_app(app=app)

    if handle_exception:
        add_exception_handler_to_app(
            app=app,
            handle_exception=handle_exception
        )
    else:
        add_exception_handler_to_app(
            app=app,
            handle_exception=simple_handle_exception
        )

    app.include_router(router=api_router)

    return app


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

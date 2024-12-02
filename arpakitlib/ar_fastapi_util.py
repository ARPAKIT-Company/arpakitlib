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
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from pydantic import BaseModel, ConfigDict
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from arpakitlib.ar_easy_sqlalchemy_util import EasySQLAlchemyDB
from arpakitlib.ar_enumeration import EasyEnumeration

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class BaseAPISchema(BaseModel):
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


class BaseAPISI(BaseAPISchema):
    pass


class BaseAPISO(BaseAPISchema):
    pass


class APISimpleDataSO(BaseAPISO):
    data: dict[str, Any] = {}


class BaseAPISimpleSO(BaseAPISO):
    id: int
    long_id: str
    creation_dt: datetime


class APIErrorSO(BaseAPISO):
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


class APIJSONResponse(fastapi.responses.JSONResponse):
    def __init__(self, *, content: BaseAPISO, status_code: int = starlette.status.HTTP_200_OK):
        super().__init__(
            content=content.model_dump(mode="json"),
            status_code=status_code
        )


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = starlette.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = APIErrorSO.APIErrorCodes.unknown_error,
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

        self.api_error_so = APIErrorSO(
            has_error=True,
            error_code=self.error_code,
            error_specification=self.error_code_specification,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.api_error_so.model_dump(mode="json")
        )


def simple_api_handle_exception(request: starlette.requests.Request, exception: Exception) -> APIJSONResponse:
    return from_exception_to_api_json_response(request=request, exception=exception)


def from_exception_to_api_json_response(
        request: starlette.requests.Request, exception: Exception
) -> APIJSONResponse:
    _logger.exception(exception)

    easy_api_error_so = APIErrorSO(
        has_error=True,
        error_code=APIErrorSO.APIErrorCodes.unknown_error
    )

    status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(exception, APIException):
        easy_api_error_so = exception.api_error_so

    elif isinstance(exception, starlette.exceptions.HTTPException):
        status_code = exception.status_code
        if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
            easy_api_error_so.error_code = APIErrorSO.APIErrorCodes.cannot_authorize
        elif status_code == starlette.status.HTTP_404_NOT_FOUND:
            easy_api_error_so.error_code = APIErrorSO.APIErrorCodes.not_found
        else:
            easy_api_error_so.error_code = APIErrorSO.APIErrorCodes.unknown_error
        if (
                isinstance(exception.detail, dict)
                or isinstance(exception.detail, list)
                or isinstance(exception.detail, str)
                or isinstance(exception.detail, int)
                or isinstance(exception.detail, float)
                or isinstance(exception.detail, bool)
        ):
            easy_api_error_so.error_data["raw"] = exception.detail

    elif isinstance(exception, fastapi.exceptions.RequestValidationError):
        status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
        easy_api_error_so.error_code = APIErrorSO.APIErrorCodes.error_in_request
        easy_api_error_so.error_data["raw"] = str(exception.errors()) if exception.errors() else {}

    else:
        status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
        easy_api_error_so.error_code = APIErrorSO.APIErrorCodes.unknown_error
        easy_api_error_so.error_data["raw"] = str(exception)
        _logger.exception(exception)

    if easy_api_error_so.error_code:
        easy_api_error_so.error_code = easy_api_error_so.error_code.upper().replace(" ", "_").strip()

    if easy_api_error_so.error_code_specification:
        easy_api_error_so.error_code_specification = (
            easy_api_error_so.error_code_specification.upper().replace(" ", "_").strip()
        )

    return APIJSONResponse(
        content=easy_api_error_so,
        status_code=status_code
    )


def add_exception_handler_to_fastapi_app(*, fastapi_app: FastAPI, api_handle_exception_: Callable) -> FastAPI:
    fastapi_app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=api_handle_exception_
    )
    fastapi_app.add_exception_handler(
        exc_class_or_status_code=ValueError,
        handler=api_handle_exception_
    )
    fastapi_app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=api_handle_exception_
    )
    fastapi_app.add_exception_handler(
        exc_class_or_status_code=starlette.exceptions.HTTPException,
        handler=api_handle_exception_
    )
    return fastapi_app


def add_middleware_cors_to_fastapi_app(*, fastapi_app: FastAPI) -> FastAPI:
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fastapi_app


def add_ar_fastapi_static_to_fastapi_app(*, fastapi_app: FastAPI):
    ar_fastapi_static_dirpath = os.path.join(str(pathlib.Path(__file__).parent), "ar_fastapi_static")
    fastapi_app.mount(
        "/ar_fastapi_static",
        StaticFiles(directory=ar_fastapi_static_dirpath),
        name="ar_fastapi_static"
    )


def add_ar_fastapi_static_docs_and_redoc_handlers_to_fastapi_app(
        *,
        fastapi_app: FastAPI,
        favicon_url: str | None = None
):
    add_ar_fastapi_static_to_fastapi_app(fastapi_app=fastapi_app)

    @fastapi_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=fastapi_app.openapi_url,
            title=fastapi_app.title,
            swagger_js_url="/ar_fastapi_static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/ar_fastapi_static/swagger-ui/swagger-ui.css",
            swagger_favicon_url=favicon_url
        )

    @fastapi_app.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=fastapi_app.openapi_url,
            title=fastapi_app.title,
            redoc_js_url="/ar_fastapi_static/redoc/redoc.standalone.js",
            redoc_favicon_url=favicon_url
        )

    return fastapi_app


class BaseAPIStartupEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info("on_startup starts")
        self._logger.info("on_startup ends")


class BaseAPIShutdownEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info("on_shutdown starts")
        self._logger.info("on_shutdown ends")


class APIStartupEventInitEasySQLAlchemyDB(BaseAPIStartupEvent):
    def __init__(self, easy_sqlalchemy_db: EasySQLAlchemyDB):
        super().__init__()
        self.easy_sqlalchemy_db = easy_sqlalchemy_db

    async def async_on_startup(self, *args, **kwargs):
        self.easy_sqlalchemy_db.init()


def create_fastapi_app(
        *,
        title: str = "ARPAKITLIB FastAPI",
        description: str | None = None,
        api_startup_events: list[BaseAPIStartupEvent] | None = None,
        api_shutdown_events: list[BaseAPIStartupEvent] | None = None,
        api_handle_exception_: Callable | None = simple_api_handle_exception
):
    if api_startup_events is None:
        api_startup_events = [BaseAPIStartupEvent()]

    if api_shutdown_events is None:
        api_shutdown_events = [BaseAPIShutdownEvent()]

    app = FastAPI(
        title=title,
        description=description,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi",
        on_startup=[api_startup_event.async_on_startup for api_startup_event in api_startup_events],
        on_shutdown=[api_shutdown_event.async_on_shutdown for api_shutdown_event in api_shutdown_events]
    )

    add_middleware_cors_to_fastapi_app(fastapi_app=app)

    add_ar_fastapi_static_docs_and_redoc_handlers_to_fastapi_app(fastapi_app=app)

    if api_handle_exception_:
        add_exception_handler_to_fastapi_app(
            fastapi_app=app,
            api_handle_exception_=api_handle_exception_
        )
    else:
        add_exception_handler_to_fastapi_app(
            fastapi_app=app,
            api_handle_exception_=simple_api_handle_exception
        )

    return app


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

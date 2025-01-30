# arpakit

from __future__ import annotations

import asyncio
import logging
import os.path
import pathlib
import traceback
from contextlib import suppress
from datetime import datetime
from typing import Any, Callable

import fastapi.exceptions
import fastapi.responses
import fastapi.security
import starlette.exceptions
import starlette.requests
import starlette.status
from fastapi import FastAPI, APIRouter, Query, Security, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_func_util import raise_if_not_async_func, is_async_function, is_async_object
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_sqlalchemy_model_util import StoryLogDBM, OperationDBM
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type, raise_if_none

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


class BaseAPIErrorCodes(Enumeration):
    cannot_authorize = "CANNOT_AUTHORIZE"
    unknown_error = "UNKNOWN_ERROR"
    error_in_request = "ERROR_IN_REQUEST"
    not_found = "NOT_FOUND"


class BaseAPIErrorSpecificationCodes(Enumeration):
    pass


class ErrorSO(BaseSO):
    has_error: bool = True
    error_code: str | None = None
    error_specification_code: str | None = None
    error_description: str | None = None
    error_data: dict[str, Any] = {}


class RawDataSO(BaseSO):
    data: dict[str, Any] = {}


class StoryLogSO(SimpleSO):
    level: str
    title: str | None
    data: dict[str, Any]

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogSO:
        return cls.model_validate(story_log_dbm.simple_dict(include_sd_properties=True))


class OperationSO(SimpleSO):
    execution_start_dt: datetime | None
    execution_finish_dt: datetime | None
    status: str
    type: str
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]
    duration_total_seconds: float | None

    @classmethod
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationSO:
        return cls.model_validate(operation_dbm.simple_dict(include_sd_properties=True))


class APIJSONResponse(fastapi.responses.JSONResponse):
    def __init__(self, *, content: dict | list | BaseSO | None, status_code: int = starlette.status.HTTP_200_OK):
        if isinstance(content, dict):
            content = safely_transfer_obj_to_json_str_to_json_obj(content)
        elif isinstance(content, list):
            content = safely_transfer_obj_to_json_str_to_json_obj(content)
        elif isinstance(content, BaseSO):
            content = safely_transfer_obj_to_json_str_to_json_obj(content.model_dump())
        elif content is None:
            content = None
        else:
            raise ValueError(f"unknown content type, type(content)={type(content)}")

        self.content_ = content
        self.status_code_ = status_code

        super().__init__(
            content=content,
            status_code=status_code
        )


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = starlette.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = BaseAPIErrorCodes.unknown_error,
            error_specification_code: str | None = None,
            error_description: str | None = None,
            error_data: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_specification_code = error_specification_code
        self.error_description = error_description
        if error_data is None:
            error_data = {}
        self.error_data = error_data

        self.error_so = ErrorSO(
            has_error=True,
            error_code=self.error_code,
            error_specification_code=self.error_specification_code,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.error_so.model_dump(mode="json")
        )


def create_handle_exception(
        *,
        funcs_before_response: list[Callable | None] | None = None,
        async_funcs_after_response: list[Callable | None] | None = None,
) -> Callable:
    if funcs_before_response is None:
        funcs_before_response = []
    funcs_before_response = [v for v in funcs_before_response if v is not None]

    if async_funcs_after_response is None:
        async_funcs_after_response = []
    async_funcs_after_response = [v for v in async_funcs_after_response if v is not None]

    async def handle_exception(
            request: starlette.requests.Request, exception: Exception
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
            _need_exc_info = False

        elif isinstance(exception, starlette.exceptions.HTTPException):
            status_code = exception.status_code
            if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
                error_so.error_code = BaseAPIErrorCodes.cannot_authorize
                _need_exc_info = False
            elif status_code == starlette.status.HTTP_404_NOT_FOUND:
                error_so.error_code = BaseAPIErrorCodes.not_found
                _need_exc_info = False
            else:
                status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
                _need_exc_info = True
            with suppress(Exception):
                error_so.error_data["exception.detail"] = exception.detail

        elif isinstance(exception, fastapi.exceptions.RequestValidationError):
            status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
            error_so.error_code = BaseAPIErrorCodes.error_in_request
            with suppress(Exception):
                error_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}
            _need_exc_info = False

        else:
            status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            error_so.error_code = BaseAPIErrorCodes.unknown_error
            _logger.exception(exception)
            _need_exc_info = True

        if error_so.error_code:
            error_so.error_code = error_so.error_code.upper().replace(" ", "_").strip()

        if error_so.error_specification_code:
            error_so.error_specification_code = (
                error_so.error_specification_code.upper().replace(" ", "_").strip()
            )

        if error_so.error_code == BaseAPIErrorCodes.not_found:
            status_code = status.HTTP_404_NOT_FOUND

        if error_so.error_code == BaseAPIErrorCodes.cannot_authorize:
            status_code = status.HTTP_401_UNAUTHORIZED

        if _need_exc_info:
            _logger.error(str(exception), exc_info=exception)
        else:
            _logger.error(str(exception))

        _kwargs = {}
        for func in funcs_before_response:
            _func_data = func(
                status_code=status_code, error_so=error_so, request=request, exception=exception, **_kwargs
            )
            if is_async_function(_func_data):
                _func_data = await _func_data
            if _func_data is not None:
                status_code, error_so, _kwargs = _func_data[0], _func_data[1], _func_data[2]
                raise_for_type(status_code, int)
                raise_for_type(error_so, ErrorSO)
                raise_for_type(_kwargs, dict)

        for async_func_after_response in async_funcs_after_response:
            raise_if_not_async_func(async_func_after_response)
            _ = asyncio.create_task(async_func_after_response(
                error_so=error_so, status_code=status_code, request=request, exception=exception
            ))

        return APIJSONResponse(
            content=error_so,
            status_code=status_code
        )

    return handle_exception


def create_story_log_before_response_in_handle_exception(
        *,
        sqlalchemy_db: SQLAlchemyDB,
        ignore_api_error_codes: list[str] | None = None,
        ignore_status_codes: list[int] | None = None
) -> Callable:
    def func(
            *,
            status_code: int,
            error_so: ErrorSO,
            request: starlette.requests.Request,
            exception: Exception,
            **kwargs
    ) -> (int, ErrorSO, dict[str, Any]):
        if ignore_api_error_codes and error_so.error_code in ignore_api_error_codes:
            return status_code, error_so, kwargs

        if ignore_status_codes and status_code in ignore_status_codes:
            return status_code, error_so, kwargs

        sqlalchemy_db.init()
        traceback_str = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        with sqlalchemy_db.new_session() as session:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=str(exception),
                data={
                    "error_so": error_so.model_dump(),
                    "traceback_str": traceback_str
                }
            )
            session.add(story_log_dbm)
            session.commit()
            session.refresh(story_log_dbm)
        error_so.error_data.update({"story_log_long_id": story_log_dbm.long_id})
        kwargs["story_log_id"] = story_log_dbm.id
        return status_code, error_so, kwargs

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


def add_cors_to_app(*, app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


class HealthcheckSO(BaseSO):
    is_ok: bool = True


def add_needed_api_router_to_app(*, app: FastAPI):
    api_router = APIRouter()

    @api_router.get(
        "/healthcheck",
        response_model=HealthcheckSO | ErrorSO,
        status_code=starlette.status.HTTP_200_OK,
        tags=["Healthcheck"]
    )
    async def _():
        return APIJSONResponse(
            status_code=starlette.status.HTTP_200_OK,
            content=HealthcheckSO(is_ok=True)
        )

    @api_router.get(
        "/arpakitlib",
        response_model=RawDataSO | ErrorSO,
        status_code=starlette.status.HTTP_200_OK,
        tags=["arpakitlib"]
    )
    async def _():
        return APIJSONResponse(
            status_code=starlette.status.HTTP_200_OK,
            content=RawDataSO(data={"arpakitlib": True})
        )

    app.include_router(router=api_router, prefix="")

    return app


class BaseStartupAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger()

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info("on_startup starts")
        self._logger.info("on_startup ends")


class BaseShutdownAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger()

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info("on_shutdown starts")
        self._logger.info("on_shutdown ends")


class BaseTransmittedAPIData(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)


def get_transmitted_api_data(request: starlette.requests.Request) -> BaseTransmittedAPIData:
    return request.app.state.transmitted_api_data


class BaseAPIAuthData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    require_api_key_string: bool = False
    require_token_string: bool = False

    require_correct_api_key: bool = False
    require_correct_token: bool = False

    token_string: str | None = None
    api_key_string: str | None = None

    is_token_correct: bool | None = None
    is_api_key_correct: bool | None = None


def base_api_auth(
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
            api_key_string: str | None = Security(APIKeyHeader(name="apikey", auto_error=False)),
            request: starlette.requests.Request,
            transmitted_api_data: BaseTransmittedAPIData = Depends(get_transmitted_api_data)
    ) -> BaseAPIAuthData:

        api_auth_data = BaseAPIAuthData(
            require_api_key_string=require_api_key_string,
            require_token_string=require_token_string,
            require_correct_api_key=require_correct_api_key,
            require_correct_token=require_correct_token
        )

        # api_key

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

        # token

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

        # api_key

        if require_api_key_string and not api_auth_data.api_key_string:
            raise APIException(
                status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                error_code=BaseAPIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # token

        if require_token_string and not api_auth_data.token_string:
            raise APIException(
                status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                error_code=BaseAPIErrorCodes.cannot_authorize,
                error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
            )

        # api_key

        if validate_api_key_func is not None:
            validate_api_key_func_data = validate_api_key_func(
                api_key_string=api_auth_data.api_key_string,
                token_string=api_auth_data.token_string,
                base_api_auth_data=api_auth_data,
                transmitted_api_data=transmitted_api_data,
                request=request,
                **kwargs
            )
            if is_async_object(validate_api_key_func_data):
                validate_api_key_func_data = await validate_api_key_func_data
            api_auth_data.is_api_key_correct = validate_api_key_func_data

        # token

        if validate_token_func is not None:
            validate_token_func_data = validate_token_func(
                api_key_string=api_auth_data.api_key_string,
                token_string=api_auth_data.token_string,
                base_api_auth_data=api_auth_data,
                transmitted_api_data=transmitted_api_data,
                request=request,
                **kwargs
            )
            if is_async_object(validate_token_func_data):
                validate_token_func_data_data = await validate_token_func_data
            api_auth_data.is_token_correct = validate_token_func_data_data

        # api_key

        if require_correct_api_key:
            if not api_auth_data.is_api_key_correct:
                raise APIException(
                    status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                    error_code=BaseAPIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_api_key_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump()),
                )

        # token

        if require_correct_token:
            if not api_auth_data.is_token_correct:
                raise APIException(
                    status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                    error_code=BaseAPIErrorCodes.cannot_authorize,
                    error_description="not api_auth_data.is_token_correct",
                    error_data=safely_transfer_obj_to_json_str_to_json_obj(api_auth_data.model_dump())
                )

        return api_auth_data

    return func


def simple_api_router_for_testing():
    router = APIRouter(tags=["Testing"])

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
        raise APIException(
            error_code="raise_fake_exception_2",
            error_specification_code="raise_fake_exception_2",
            error_description="raise_fake_exception_2"
        )

    @router.get(
        "/raise_fake_exception_3",
        response_model=ErrorSO
    )
    async def _():
        raise Exception("raise_fake_exception_3")

    @router.get(
        "/check_params_1",
        response_model=ErrorSO
    )
    async def _(name: int = Query()):
        return RawDataSO(data={"name": name})

    return router


def create_fastapi_app(
        *,
        title: str = "arpakitlib FastAPI",
        description: str | None = "arpakitlib FastAPI",
        log_filepath: str | None = "./story.log",
        handle_exception_: Callable | None = None,
        startup_api_events: list[BaseStartupAPIEvent | None] | None = None,
        shutdown_api_events: list[BaseShutdownAPIEvent | None] | None = None,
        transmitted_api_data: BaseTransmittedAPIData = BaseTransmittedAPIData(),
        main_api_router: APIRouter = simple_api_router_for_testing(),
        contact: dict[str, Any] | None = None,
        media_dirpath: str | None = None,
        static_dirpath: str | None = None
):
    _logger.info("start create_fastapi_app")

    setup_normal_logging(log_filepath=log_filepath)

    if handle_exception_ is None:
        handle_exception_ = create_handle_exception()

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
        contact=contact
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
        handle_exception=handle_exception_
    )

    add_needed_api_router_to_app(app=app)

    app.include_router(router=main_api_router)

    _logger.info("finish create_fastapi_app")

    return app


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

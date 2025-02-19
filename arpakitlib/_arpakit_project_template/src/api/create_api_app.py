import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.api.event import get_api_startup_events, get_api_shutdown_events
from src.api.exception_handler import add_exception_handler_to_app
from src.api.openapi_ui import add_local_openapi_to_app
from src.api.router.main_router import main_api_router
from src.api.transmitted_api_data import get_cached_transmitted_api_data
from src.core.const import ProjectPaths
from src.core.util import setup_logging

_logger = logging.getLogger(__name__)


def create_api_app() -> FastAPI:
    setup_logging()

    _logger.info("start")

    transmitted_api_data = get_cached_transmitted_api_data()

    api_app = FastAPI(
        title=transmitted_api_data.settings.project_name,
        description=transmitted_api_data.settings.project_name,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi",
        on_startup=get_api_startup_events(),
        on_shutdown=get_api_shutdown_events(),
        contact={
            "name": "ARPAKIT Company",
            "url": "https://arpakit.com/",
            "email": "support@arpakit.com",
        },
    )

    api_app.state.transmitted_api_data = transmitted_api_data

    if transmitted_api_data.settings.media_dirpath is not None:
        if not os.path.exists(transmitted_api_data.settings.media_dirpath):
            os.makedirs(transmitted_api_data.settings.media_dirpath, exist_ok=True)
        api_app.mount("/media", StaticFiles(directory=transmitted_api_data.settings.media_dirpath), name="media")

    if not os.path.exists(ProjectPaths.static_dirpath):
        os.makedirs(ProjectPaths.static_dirpath, exist_ok=True)
    api_app.mount("/static", StaticFiles(directory=ProjectPaths.static_dirpath), name="static")

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_local_openapi_to_app(app=api_app)

    add_exception_handler_to_app(app=api_app)

    api_app.include_router(router=main_api_router)

    if transmitted_api_data.settings.api_enable_admin1:
        from src.admin1.add_admin_in_app import add_admin1_in_app
        add_admin1_in_app(app=api_app)

    _logger.info("finish")

    return api_app

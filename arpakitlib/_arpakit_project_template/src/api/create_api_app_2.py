from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from arpakitlib.ar_fastapi_util import create_fastapi_app
from src.api.event import get_startup_api_events, get_shutdown_api_events
from src.api.exception_handler import create_exception_handler_
from src.api.router.main_router import main_api_router
from src.api.transmitted_api_data import get_cached_transmitted_api_data
from src.core.const import ProjectPaths
from src.core.util import setup_logging


def create_api_app() -> FastAPI:
    setup_logging()

    transmitted_api_data = get_cached_transmitted_api_data()

    exception_handler = create_exception_handler_(transmitted_api_data=transmitted_api_data)

    startup_api_events = get_startup_api_events(transmitted_api_data=transmitted_api_data)

    shutdown_api_events = get_shutdown_api_events(transmitted_api_data=transmitted_api_data)

    api_app = create_fastapi_app(
        title=transmitted_api_data.settings.project_name,
        description=transmitted_api_data.settings.project_name,
        exception_handler=exception_handler,
        startup_api_events=startup_api_events,
        shutdown_api_events=shutdown_api_events,
        transmitted_api_data=transmitted_api_data,
        main_api_router=main_api_router,
        media_dirpath=transmitted_api_data.settings.media_dirpath,
        static_dirpath=ProjectPaths.static_dirpath
    )

    if media_dirpath is not None:
        if not os.path.exists(media_dirpath):
            os.makedirs(media_dirpath, exist_ok=True)
        app.mount("/media", StaticFiles(directory=media_dirpath), name="media")

    if static_dirpath is not None:
        if not os.path.exists(static_dirpath):
            os.makedirs(static_dirpath, exist_ok=True)
        app.mount("/static", StaticFiles(directory=static_dirpath), name="static")

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if transmitted_api_data.settings.api_enable_admin1:
        from src.admin1.add_admin_in_app import add_admin1_in_app
        add_admin1_in_app(app=api_app)

    return api_app


if __name__ == '__main__':
    create_api_app()

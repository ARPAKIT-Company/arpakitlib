from fastapi import FastAPI

from arpakitlib.ar_fastapi_util import create_fastapi_app
from src.api.create_handle_exception_ import create_handle_exception_
from src.api.event import get_startup_api_events, get_shutdown_api_events
from src.api.router.main_router import main_api_router
from src.api.util import get_transmitted_api_data
from src.core.const import ProjectPaths
from src.core.util import setup_logging


def create_api_app() -> FastAPI:
    setup_logging()

    transmitted_api_data = get_transmitted_api_data()

    handle_exception_ = create_handle_exception_(transmitted_api_data=transmitted_api_data)

    startup_api_events = get_startup_api_events(transmitted_api_data=transmitted_api_data)

    shutdown_api_events = get_shutdown_api_events(transmitted_api_data=transmitted_api_data)

    api_app = create_fastapi_app(
        title=transmitted_api_data.settings.project_name,
        description=transmitted_api_data.settings.project_name,
        handle_exception_=handle_exception_,
        startup_api_events=startup_api_events,
        shutdown_api_events=shutdown_api_events,
        transmitted_api_data=transmitted_api_data,
        main_api_router=main_api_router,
        media_dirpath=transmitted_api_data.settings.media_dirpath,
        static_dirpath=ProjectPaths.static_dirpath
    )

    if transmitted_api_data.settings.api_enable_admin1:
        from src.admin1.add_admin_in_app import add_admin1_in_app
        add_admin1_in_app(app=api_app)

    return api_app


if __name__ == '__main__':
    create_api_app()

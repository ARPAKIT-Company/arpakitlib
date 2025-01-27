from fastapi import FastAPI
from starlette import status

from arpakitlib.ar_fastapi_util import create_fastapi_app, \
    create_handle_exception, create_story_log_before_response_in_handle_exception
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type
from src.api.const import APIErrorCodes
from src.api.event import StartupAPIEvent, ShutdownAPIEvent
from src.api.router.main_router import main_api_router
from src.api.transmitted_api_data import TransmittedAPIData
from src.core.const import ProjectPaths
from src.core.settings import get_cached_settings
from src.core.util import setup_logging, get_cached_media_file_storage_in_dir, get_cached_cache_file_storage_in_dir, \
    get_cached_dump_file_storage_in_dir
from src.db.util import get_cached_sqlalchemy_db


def create_api_app() -> FastAPI:
    setup_logging()

    settings = get_cached_settings()

    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sql_db_url is not None else None

    transmitted_api_data = TransmittedAPIData(
        settings=settings,
        sqlalchemy_db=sqlalchemy_db,
        media_file_storage_in_dir=get_cached_media_file_storage_in_dir(),
        cache_file_storage_in_dir=get_cached_cache_file_storage_in_dir(),
        dump_file_storage_in_dir=get_cached_dump_file_storage_in_dir()
    )

    funcs_before_response = []

    if settings.api_create_story_log_before_response_in_handle_exception:
        raise_for_type(sqlalchemy_db, SQLAlchemyDB)
        funcs_before_response.append(
            create_story_log_before_response_in_handle_exception(
                sqlalchemy_db=sqlalchemy_db,
                ignore_api_error_codes=[APIErrorCodes.not_found],
                ignore_status_codes=[status.HTTP_404_NOT_FOUND]
            )
        )

    handle_exception = create_handle_exception(
        funcs_before_response=funcs_before_response,
        async_funcs_after_response=[]
    )

    startup_api_events = []

    startup_api_events.append(StartupAPIEvent(transmitted_api_data=transmitted_api_data))

    shutdown_api_events = []

    shutdown_api_events.append(ShutdownAPIEvent(transmitted_api_data=transmitted_api_data))

    api_app = create_fastapi_app(
        title=settings.api_title.strip(),
        description=settings.api_description.strip(),
        log_filepath=settings.log_filepath,
        handle_exception_=handle_exception,
        startup_api_events=startup_api_events,
        shutdown_api_events=shutdown_api_events,
        transmitted_api_data=transmitted_api_data,
        main_api_router=main_api_router,
        media_dirpath=settings.media_dirpath,
        static_dirpath=ProjectPaths.static_dirpath
    )

    if settings.api_enable_admin1:
        from src.admin1.add_admin_in_app import add_admin1_in_app
        add_admin1_in_app(app=api_app)

    return api_app


if __name__ == '__main__':
    create_api_app()

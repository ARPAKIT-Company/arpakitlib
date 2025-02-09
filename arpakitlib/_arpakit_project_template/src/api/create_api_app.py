from fastapi import FastAPI

from arpakitlib.ar_fastapi_util import create_fastapi_app
from src.api.create_handle_exception_ import create_handle_exception_
from src.api.event import get_startup_api_events, get_shutdown_api_events
from src.api.router.main_router import main_api_router
from src.api.transmitted_api_data import TransmittedAPIData
from src.core.const import ProjectPaths
from src.core.settings import get_cached_settings
from src.core.util import setup_logging, get_cached_media_file_storage_in_dir, get_cached_cache_file_storage_in_dir, \
    get_cached_dump_file_storage_in_dir
from src.json_db.util import get_json_db
from src.sql_db.util import get_cached_sqlalchemy_db


def create_api_app() -> FastAPI:
    setup_logging()

    settings = get_cached_settings()

    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sync_sql_db_url is not None else None

    json_db = get_json_db() if settings.json_db_dirpath is not None else None

    media_file_storage_in_dir = (
        get_cached_media_file_storage_in_dir() if settings.media_dirpath is not None else None
    )

    cache_file_storage_in_dir = (
        get_cached_cache_file_storage_in_dir() if settings.cache_dirpath is not None else None
    )

    dump_file_storage_in_dir = (
        get_cached_dump_file_storage_in_dir() if settings.dump_dirpath is not None else None
    )

    transmitted_api_data = TransmittedAPIData(
        sqlalchemy_db=sqlalchemy_db,
        json_db=json_db,
        media_file_storage_in_dir=media_file_storage_in_dir,
        cache_file_storage_in_dir=cache_file_storage_in_dir,
        dump_file_storage_in_dir=dump_file_storage_in_dir,
        settings=settings
    )

    handle_exception_ = create_handle_exception_(transmitted_api_data=transmitted_api_data)

    startup_api_events = get_startup_api_events(transmitted_api_data=transmitted_api_data)

    shutdown_api_events = get_shutdown_api_events(transmitted_api_data=transmitted_api_data)

    api_app = create_fastapi_app(
        title=settings.project_name.strip(),
        description=settings.project_name.strip(),
        handle_exception_=handle_exception_,
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

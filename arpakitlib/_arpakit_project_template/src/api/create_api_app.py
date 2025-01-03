from fastapi import FastAPI

from arpakitlib.ar_fastapi_util import create_fastapi_app, InitSqlalchemyDBStartupAPIEvent, InitFileStoragesInDir, \
    create_handle_exception, create_handle_exception_creating_story_log
from src.api.event import FirstStartupAPIEvent, FirstShutdownAPIEvent
from src.api.router.v1.main_router import api_v1_main_router
from src.api.transmitted_api_data import TransmittedAPIData
from src.core.settings import get_cached_settings
from src.core.util import get_cached_sqlalchemy_db, get_cached_media_file_storage_in_dir, \
    get_cached_cache_file_storage_in_dir, get_cached_dump_file_storage_in_dir, setup_logging


def create_api_app() -> FastAPI:
    setup_logging()

    settings = get_cached_settings()
    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sql_db_url is not None else None

    transmitted_api_data = TransmittedAPIData(
        settings=get_cached_settings(),
        sqlalchemy_db=sqlalchemy_db
    )

    api_app = create_fastapi_app(
        title="{PROJECT_NAME}",
        description="{PROJECT_NAME}",
        log_filepath=get_cached_settings().log_filepath,
        handle_exception_=create_handle_exception(
            funcs_before_response=[
                create_handle_exception_creating_story_log(sqlalchemy_db=sqlalchemy_db)
                if sqlalchemy_db is not None else None
            ],
            async_funcs_after_response=[]
        ),
        startup_api_events=[
            FirstStartupAPIEvent(transmitted_api_data=transmitted_api_data),
            InitFileStoragesInDir(
                file_storages_in_dir=[
                    get_cached_media_file_storage_in_dir(),
                    get_cached_cache_file_storage_in_dir(),
                    get_cached_dump_file_storage_in_dir()
                ]
            ),
            (
                InitSqlalchemyDBStartupAPIEvent(sqlalchemy_db=sqlalchemy_db)
                if (sqlalchemy_db is not None and settings.init_sql_db_at_start) else None
            ),
        ],
        shutdown_api_events=[
            FirstShutdownAPIEvent(transmitted_api_data=transmitted_api_data)
        ],
        transmitted_api_data=transmitted_api_data,
        main_api_router=api_v1_main_router,
        media_dirpath=settings.media_dirpath
    )

    return api_app


if __name__ == '__main__':
    create_api_app()

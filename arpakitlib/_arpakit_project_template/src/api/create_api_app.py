from fastapi import FastAPI

from arpakitlib.ar_base_worker_util import SafeRunInBackgroundModes
from arpakitlib.ar_fastapi_util import create_fastapi_app, InitSqlalchemyDBStartupAPIEvent, InitFileStoragesInDir, \
    create_handle_exception, create_story_log_before_response_in_handle_exception, DEFAULT_CONTACT, \
    SafeRunWorkerStartupAPIEvent
from arpakitlib.ar_operation_execution_util import OperationExecutorWorker, ScheduledOperationCreatorWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type
from src.api.event import StartupAPIEvent, ShutdownAPIEvent
from src.api.router.main_router import main_api_router
from src.api.transmitted_api_data import TransmittedAPIData
from src.core.const import STATIC_DIRPATH
from src.core.settings import get_cached_settings
from src.core.util import get_cached_media_file_storage_in_dir, \
    get_cached_cache_file_storage_in_dir, get_cached_dump_file_storage_in_dir, setup_logging
from src.db.util import get_cached_sqlalchemy_db
from src.operation_execution.operation_executor import OperationExecutor
from src.operation_execution.scheduled_operations import ALL_SCHEDULED_OPERATIONS


def create_api_app() -> FastAPI:
    setup_logging()

    settings = get_cached_settings()

    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sql_db_url is not None else None

    transmitted_api_data = TransmittedAPIData(
        settings=settings,
        sqlalchemy_db=sqlalchemy_db
    )

    funcs_before_response = []

    if settings.api_create_story_log_before_response_in_handle_exception:
        raise_for_type(sqlalchemy_db, SQLAlchemyDB)
        funcs_before_response.append(
            create_story_log_before_response_in_handle_exception(
                sqlalchemy_db=sqlalchemy_db,
                ignore_api_error_code_not_found=True
            )
        )

    handle_exception = create_handle_exception(
        funcs_before_response=funcs_before_response,
        async_funcs_after_response=[]
    )

    startup_api_events = []

    startup_api_events.append(InitFileStoragesInDir(
        file_storages_in_dir=[
            get_cached_media_file_storage_in_dir() if settings.media_dirpath is not None else None,
            get_cached_cache_file_storage_in_dir() if settings.cache_dirpath is not None else None,
            get_cached_dump_file_storage_in_dir() if settings.dump_dirpath is not None else None
        ]
    ))

    if settings.api_init_sql_db_at_start:
        raise_for_type(sqlalchemy_db, SQLAlchemyDB)
        startup_api_events.append(InitSqlalchemyDBStartupAPIEvent(sqlalchemy_db=sqlalchemy_db))

    startup_api_events.append(StartupAPIEvent(transmitted_api_data=transmitted_api_data))

    if settings.api_start_operation_executor_worker:
        raise_for_type(sqlalchemy_db, SQLAlchemyDB)
        startup_api_events.append(
            SafeRunWorkerStartupAPIEvent(
                workers=[
                    OperationExecutorWorker(
                        sqlalchemy_db=sqlalchemy_db,
                        operation_executor=OperationExecutor(sqlalchemy_db=sqlalchemy_db),
                        filter_operation_types=None
                    )
                ],
                safe_run_in_background_mode=SafeRunInBackgroundModes.async_task
            )
        )

    if settings.api_start_scheduled_operation_creator_worker:
        raise_for_type(sqlalchemy_db, SQLAlchemyDB)
        startup_api_events.append(
            SafeRunWorkerStartupAPIEvent(
                workers=[
                    ScheduledOperationCreatorWorker(
                        sqlalchemy_db=sqlalchemy_db,
                        scheduled_operations=ALL_SCHEDULED_OPERATIONS
                    )
                ],
                safe_run_in_background_mode=SafeRunInBackgroundModes.async_task
            )
        )

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
        contact=DEFAULT_CONTACT,
        media_dirpath=settings.media_dirpath,
        static_dirpath=STATIC_DIRPATH
    )

    return api_app


if __name__ == '__main__':
    create_api_app()

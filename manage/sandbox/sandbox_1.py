import asyncio

import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app, create_handle_exception, ErrorSO, \
    create_handle_exception_creating_story_log, InitSqlalchemyDBStartupAPIEvent, \
    AsyncSafeRunExecuteOperationWorkerStartupAPIEvent, SyncSafeRunExecuteOperationWorkerStartupAPIEvent
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import ExecuteOperationWorker
from arpakitlib.ar_sleep_util import async_safe_sleep
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB


async def f(error_so: ErrorSO, status_code: int, **kwargs):
    print("2st4wtwetwest")
    return status_code, error_so


def command():
    setup_normal_logging()

    sqlalchemy_db = SQLAlchemyDB()
    sqlalchemy_db.drop()

    app = create_fastapi_app(
        startup_api_events=[
            InitSqlalchemyDBStartupAPIEvent(sqlalchemy_db=sqlalchemy_db),
            SyncSafeRunExecuteOperationWorkerStartupAPIEvent(
                execute_operation_worker=ExecuteOperationWorker(
                    sqlalchemy_db=sqlalchemy_db,
                )
            ),
            AsyncSafeRunExecuteOperationWorkerStartupAPIEvent(
                execute_operation_worker=ExecuteOperationWorker(
                    sqlalchemy_db=sqlalchemy_db,
                    filter_operation_type="healthcheck"
                )
            )
        ],
        handle_exception_=create_handle_exception(
            funcs_before_response=[
                create_handle_exception_creating_story_log(sqlalchemy_db=sqlalchemy_db)
            ]
        )
    )
    uvicorn.run(app=app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

import asyncio

import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app, create_handle_exception, ErrorSO, \
    create_handle_exception_creating_story_log, InitSqlalchemyDBStartupAPIEvent, \
    AsyncSafeRunExecuteOperationWorkerStartupAPIEvent, SyncSafeRunExecuteOperationWorkerStartupAPIEvent, \
    BaseStartupAPIEvent
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import ExecuteOperationWorker, BaseOperationExecutor
from arpakitlib.ar_sleep_util import async_safe_sleep
from arpakitlib.ar_sqlalchemy_model_util import OperationDBM
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_yookassa_api_client_util import YookassaAPIClient


async def f(error_so: ErrorSO, status_code: int, **kwargs):
    print("2st4wtwetwest")
    return status_code, error_so



class OperationExecutor(BaseOperationExecutor):
    async def async_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        if operation_dbm.type == "healthcheck":
            open("./file.txt", mode="a").write(f"{operation_dbm.id}\n\n")


def command():
    setup_normal_logging()

    sqlalchemy_db = SQLAlchemyDB()
    sqlalchemy_db.drop()

    class Startup1(BaseStartupAPIEvent):
        async def async_on_startup(self, *args, **kwargs):
            open("./file.txt", mode="w").write(f"")

    class Startup(BaseStartupAPIEvent):
        async def async_on_startup(self, *args, **kwargs):
            open("./file.txt", mode="w").write(f"start\n\n")

    app = create_fastapi_app(
        startup_api_events=[
            InitSqlalchemyDBStartupAPIEvent(sqlalchemy_db=sqlalchemy_db),
            AsyncSafeRunExecuteOperationWorkerStartupAPIEvent(
                execute_operation_worker=ExecuteOperationWorker(
                    sqlalchemy_db=sqlalchemy_db,
                    operation_executor=OperationExecutor(sqlalchemy_db=sqlalchemy_db)
                )
            ),
            Startup1(),
            Startup()
        ],
        handle_exception_=create_handle_exception(
            funcs_before_response=[
                create_handle_exception_creating_story_log(sqlalchemy_db=sqlalchemy_db)
            ]
        )
    )

    @app.get("/create_healthcheck")
    async def _():
        with sqlalchemy_db.new_session() as session:
            session.add(OperationDBM(
                type="healthcheck",
            ))
            session.commit()
        return {}

    uvicorn.run(app=app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

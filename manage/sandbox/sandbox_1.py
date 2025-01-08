import asyncio

from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import OperationExecutorWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.operation_execution.operation_executor import OperationExecutor


class A(OperationExecutorWorker):
    async def async_on_startup(self):
        raise Exception


def command():
    pass

async def async_command():
    setup_normal_logging(log_filepath="./story.log")
    await A(
        sqlalchemy_db=SQLAlchemyDB(
            db_url="postgresql://arpakitlib:arpakitlib@127.0.0.1:50517/arpakitlib"
        ),
        operation_executor=OperationExecutor(
            sqlalchemy_db=SQLAlchemyDB(
                db_url="postgresql://arpakitlib:arpakitlib@127.0.0.1:50517/arpakitlib"
            )
        )
    ).async_safe_run()


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

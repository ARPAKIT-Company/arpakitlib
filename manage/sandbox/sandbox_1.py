import asyncio
import logging

from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import OperationExecutorWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from manage.sandbox.hgjk.g import go
from src.operation_execution.operation_executor import OperationExecutor


class A(OperationExecutorWorker):
    pass


def command():
    setup_normal_logging()
    go()

async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

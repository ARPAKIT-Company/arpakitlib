from core.util import setup_logging
from operation_execution.operation_executor_worker import OperationExecutorWorker
from sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    worker = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    __command()

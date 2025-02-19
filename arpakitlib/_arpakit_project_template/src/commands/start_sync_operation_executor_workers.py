from arpakitlib.ar_base_worker_util import safe_run_workers_in_background, SafeRunInBackgroundModes
from src.core.util import setup_logging
from src.operation_execution.operation_executor_worker import OperationExecutorWorker
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    worker_1 = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    worker_2 = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    worker_3 = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    worker_4 = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    safe_run_workers_in_background(
        workers=[worker_1, worker_2, worker_3, worker_4],
        mode=SafeRunInBackgroundModes.thread
    )
    input("press to close")


if __name__ == '__main__':
    __command()

from src.core.util import setup_logging
from src.operation_execution.operation_executor_worker import OperationExecutorWorker
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def __just_script():
    setup_logging()
    worker = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    __just_script()

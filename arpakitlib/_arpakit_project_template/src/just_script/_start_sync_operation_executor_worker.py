from src.core.util import setup_logging
from src.operation_execution.operation_execution_logic import OperationExecutionLogic
from src.operation_execution.operation_executor_worker import OperationExecutorWorker
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def _start_operation_executor_worker():
    setup_logging()
    worker = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        operation_executor=OperationExecutionLogic(sqlalchemy_db=get_cached_sqlalchemy_db())
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    _start_operation_executor_worker()

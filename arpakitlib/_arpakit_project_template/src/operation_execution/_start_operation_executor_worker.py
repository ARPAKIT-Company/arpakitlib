from arpakitlib.ar_operation_execution_util import OperationExecutorWorker
from src.core.util import setup_logging
from src.db.util import get_cached_sqlalchemy_db
from src.operation_execution.operation_executor import OperationExecutor


def _start_operation_executor_worker():
    setup_logging()
    worker = OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        operation_executor=OperationExecutor(sqlalchemy_db=get_cached_sqlalchemy_db())
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    _start_operation_executor_worker()

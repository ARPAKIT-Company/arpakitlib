from arpakitlib.ar_operation_execution_util import ExecuteOperationWorker
from src.core.util import get_cached_sqlalchemy_db, setup_logging
from src.operation_execution.operation_executor import OperationExecutor


def start_operation_executor_for_dev():
    setup_logging()
    worker = ExecuteOperationWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        operation_executor=OperationExecutor(sqlalchemy_db=get_cached_sqlalchemy_db()),
        filter_operation_types=None
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    start_operation_executor_for_dev()

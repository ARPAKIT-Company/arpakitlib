from arpakitlib.ar_operation_execution_util import ScheduledOperationCreatorWorker
from src.core.util import setup_logging
from src.operation_execution.scheduled_operations import SCHEDULED_OPERATIONS
from src.sql_db.util import get_cached_sqlalchemy_db


def _start_scheduled_operation_creator_worker():
    setup_logging()
    worker = ScheduledOperationCreatorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        scheduled_operations=SCHEDULED_OPERATIONS
    )
    worker.sync_safe_run()


if __name__ == '__main__':
    _start_scheduled_operation_creator_worker()

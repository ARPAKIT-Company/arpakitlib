from datetime import timedelta
from functools import lru_cache

from arpakitlib.ar_operation_execution_util import ScheduledOperationCreatorWorker
from src.db.util import get_cached_sqlalchemy_db


def create_scheduled_operation_creator_worker() -> ScheduledOperationCreatorWorker:
    from src.operation_execution.scheduled_operations import ALL_SCHEDULED_OPERATIONS
    scheduled_operation_creator_worker = ScheduledOperationCreatorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        scheduled_operations=ALL_SCHEDULED_OPERATIONS,
        timeout_after_run=timedelta(seconds=0.1).total_seconds(),
        timeout_after_err_in_run=timedelta(seconds=1).total_seconds()
    )
    return scheduled_operation_creator_worker


@lru_cache()
def get_scheduled_operation_creator_worker() -> ScheduledOperationCreatorWorker:
    return create_scheduled_operation_creator_worker()

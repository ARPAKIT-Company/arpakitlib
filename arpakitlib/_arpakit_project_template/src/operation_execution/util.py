from functools import lru_cache

from arpakitlib.ar_operation_execution_util import ScheduledOperationCreatorWorker
from src.db.util import get_cached_sqlalchemy_db


def create_scheduled_operation_creator_worker() -> ScheduledOperationCreatorWorker:
    from src.operation_execution.scheduled_operations import SCHEDULED_OPERATIONS
    scheduled_operation_creator_worker = ScheduledOperationCreatorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        scheduled_operations=SCHEDULED_OPERATIONS,
        startup_funcs=[
            get_cached_sqlalchemy_db().init
        ]
    )
    return scheduled_operation_creator_worker


@lru_cache()
def get_scheduled_operation_creator_worker() -> ScheduledOperationCreatorWorker:
    return create_scheduled_operation_creator_worker()

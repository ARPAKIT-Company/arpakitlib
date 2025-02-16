import asyncio

from src.core.util import setup_logging
from src.operation_execution.scheduled_operation_creator_worker import ScheduledOperationCreatorWorker
from src.operation_execution.scheduled_operations import SCHEDULED_OPERATIONS
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


async def _start_async_scheduled_operation_creator_worker():
    setup_logging()
    worker = ScheduledOperationCreatorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        scheduled_operations=SCHEDULED_OPERATIONS
    )
    await worker.async_safe_run()


if __name__ == '__main__':
    asyncio.run(_start_async_scheduled_operation_creator_worker())

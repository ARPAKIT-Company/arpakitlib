import asyncio

from core.util import setup_logging
from operation_execution.scheduled_operation_creator_worker import create_scheduled_operation_creator_worker


async def __command():
    setup_logging()
    worker = create_scheduled_operation_creator_worker()
    await worker.async_safe_run()


if __name__ == '__main__':
    asyncio.run(__command())

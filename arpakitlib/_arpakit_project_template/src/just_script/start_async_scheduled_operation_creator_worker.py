import asyncio

from src.core.util import setup_logging
from src.operation_execution.scheduled_operation_creator_worker import create_scheduled_operation_creator_worker


async def __just_script():
    setup_logging()
    worker = create_scheduled_operation_creator_worker()
    await worker.async_safe_run()


if __name__ == '__main__':
    asyncio.run(__just_script())

import asyncio

from src.core.util import setup_logging
from src.operation_execution.operation_executor_worker import create_operation_executor_worker


def __just_script():
    setup_logging()
    worker = create_operation_executor_worker()
    asyncio.run(worker.async_safe_run())


if __name__ == '__main__':
    __just_script()

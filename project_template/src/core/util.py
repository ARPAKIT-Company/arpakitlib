import asyncio

from arpakitlib.ar_logging_util import setup_normal_logging
from project_template.src.core.settings import get_cached_settings


def setup_logging():
    setup_normal_logging(log_filepath=get_cached_settings().log_filepath)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

# arpakit

import asyncio
import logging
import math
from time import sleep

from asyncpg.pgproto.pgproto import timedelta

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def sync_safe_sleep(n: timedelta | float | int):
    _logger.info(f"sync_safe_sleep ({n}) starts")

    if isinstance(n, timedelta):
        n = n.total_seconds()
    elif isinstance(n, int):
        n = float(n)
    elif isinstance(n, float):
        n = n
    else:
        raise TypeError(f"n={n}, type={type(n)}, n: timedelta | float | int")

    n: float = n

    frac, int_part = math.modf(n)
    for i in range(int(int_part)):
        sleep(1)
    sleep(frac)

    _logger.info(f"sync_safe_sleep ({n}) ends")


async def async_safe_sleep(n: timedelta | float | int):
    _logger.info(f"async_safe_sleep ({n}) starts")

    if isinstance(n, timedelta):
        n = n.total_seconds()
    elif isinstance(n, int):
        n = float(n)
    elif isinstance(n, float):
        n = n
    else:
        raise TypeError(f"n={n}, type={type(n)}, n: timedelta | float | int")

    n: float = n

    _logger.info(f"sleep_time ({n}) starts")
    await asyncio.sleep(n)
    _logger.info(f"sleep_time ({n}) ends")

    _logger.info(f"async_safe_sleep ({n}) ends")


def __example():
    print("sync hello in 2 seconds...")
    sync_safe_sleep(n=timedelta(seconds=2))
    print("sync hello world!")


async def __async_example():
    print("async hello in 0.5 seconds...")
    await async_safe_sleep(n=timedelta(seconds=0.5))
    print("async hello world!")


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

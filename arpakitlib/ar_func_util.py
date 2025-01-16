import asyncio
import inspect
from typing import Callable

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def is_async_function(func: Callable) -> bool:
    return asyncio.iscoroutinefunction(func)


def is_async_object(obj: object) -> bool:
    return asyncio.iscoroutine(obj)


def is_sync_function(func: Callable) -> bool:
    return inspect.isfunction(func) and not is_async_function(func)


def raise_if_not_async_func(func: Callable):
    if not is_async_function(func):
        raise TypeError(f"The provided function '{func.__name__}' is not an async function")


def raise_if_not_sync_func(func: Callable):
    if not is_sync_function(func):
        raise TypeError(f"The provided function '{func.__name__}' is not a sync function")


def raise_if_async_func(func: Callable):
    if is_async_function(func):
        raise TypeError(f"The provided function '{func.__name__}' should not be async")


def raise_if_sync_func(func: Callable):
    if is_sync_function(func):
        raise TypeError(f"The provided function '{func.__name__}' should not be sync")


def __example():
    def one():
        pass

    async def two():
        pass

    print(is_sync_function(one))
    print(is_sync_function(two))

    print(is_async_function(one))
    print(is_async_function(two))


if __name__ == '__main__':
    __example()

import asyncio
import inspect
from typing import Callable

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def is_async_callable(obj: Callable) -> bool:
    if inspect.ismethod(obj) or inspect.isfunction(obj):
        return inspect.iscoroutinefunction(obj)
    if isinstance(obj, (staticmethod, classmethod)):
        return inspect.iscoroutinefunction(obj.__func__)
    return False


def raise_if_not_async_callable(obj: Callable):
    if not is_async_callable(obj):
        raise TypeError(f"The provided callable '{obj.__name__}' is not an async")


# ---


def is_async_object(obj: object) -> bool:
    return asyncio.iscoroutine(obj)


# ---


def is_sync_function(obj: Callable) -> bool:
    return callable(obj) and not is_async_callable(obj=obj)


def raise_if_not_sync_callable(obj: Callable):
    if not is_sync_function(obj):
        raise TypeError(f"The provided callable '{obj.__name__}' is not an sync")


def __example():
    pass


if __name__ == '__main__':
    __example()

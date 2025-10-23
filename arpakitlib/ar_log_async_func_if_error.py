# arpakit

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

import logging

_logger = logging.getLogger()


async def log_async_func_if_error(async_func, **kwargs):
    try:
        await async_func(**kwargs)
    except Exception as exception:
        _logger.error(
            f"error in async_func, {async_func.__name__=}",
            exc_info=exception,
            extra={
                "log_async_func_if_error": True,
                "async_func_name": async_func.__name__
            }
        )

import asyncio

import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app, create_handle_exception, ErrorSO
from arpakitlib.ar_sleep_util import async_safe_sleep


async def f(error_so: ErrorSO, status_code: int, **kwargs):
    print("2st4wtwetwest")
    return status_code, error_so


def command():
    app = create_fastapi_app(
        handle_exception_=create_handle_exception(
            funcs_before_response=[lambda **kwargs: print("1"), lambda **kwargs: print("3")],
            async_funcs_after_response=[f]
        )
    )
    uvicorn.run(app=app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

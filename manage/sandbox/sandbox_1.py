import asyncio

import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app


def command():
    app = create_fastapi_app()
    uvicorn.run(app=app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

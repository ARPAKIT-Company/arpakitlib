import asyncio

import uvicorn
from fastapi import Depends
from pydantic import BaseModel

from arpakitlib.ar_fastapi_util import create_fastapi_app, check_api_key_api_auth, CheckAPIKeyAPIAuthData


def command():
    api_app = create_fastapi_app()

    @api_app.get("/check1")
    async def _(
            check_api_key_api_auth_data: CheckAPIKeyAPIAuthData = Depends(check_api_key_api_auth(
                require_check_api_key=True, correct_api_key="1"
            ))
    ):
        return check_api_key_api_auth_data

    @api_app.get("/check2")
    async def _(
            check_api_key_api_auth_data: CheckAPIKeyAPIAuthData = Depends(check_api_key_api_auth(
                require_check_api_key=False, check_api_key_func=lambda d: d == "1"
            ))
    ):
        return check_api_key_api_auth_data

    uvicorn.run(app=api_app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

import asyncio

import uvicorn
from fastapi import Depends

from arpakitlib.ar_fastapi_util import create_fastapi_app, BaseNeedAPIAuthData, base_need_api_auth


def command():
    app = create_fastapi_app()

    @app.get("/hello")
    async def _(need_api_auth_data: BaseNeedAPIAuthData = Depends(base_need_api_auth(require_token_string=True, require_api_key_string=True))):
        pass
    uvicorn.run(app=app)



async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

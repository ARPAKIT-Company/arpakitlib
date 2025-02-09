import uvicorn
from fastapi import Depends

from arpakitlib.ar_fastapi_util import create_fastapi_app, base_api_auth

app = create_fastapi_app()

@app.get("/")
async def _(*args, auth=Depends(base_api_auth()), **kwargs):
    pass


uvicorn.run(
    app=app
)

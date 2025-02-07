import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app

app = create_fastapi_app()


uvicorn.run(app=app, port=50519, host="127.0.0.1")

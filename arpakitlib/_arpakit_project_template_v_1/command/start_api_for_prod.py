import uvicorn

from core.settings import get_cached_settings
from core.util import setup_logging


def __command():
    setup_logging()
    uvicorn.run(
        app="api.asgi:app",
        host="127.0.0.1",
        port=get_cached_settings().api_port,
        reload=False,
        workers=4
    )


if __name__ == '__main__':
    __command()

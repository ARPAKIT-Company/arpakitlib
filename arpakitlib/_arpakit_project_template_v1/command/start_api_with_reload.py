import uvicorn

from core.settings import get_cached_settings
from core.util import setup_logging


def __command():
    setup_logging()
    uvicorn.run(
        "api.asgi:app",
        port=get_cached_settings().api_port,
        host="localhost",
        workers=1,
        reload=True
    )


if __name__ == '__main__':
    __command()

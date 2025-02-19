import uvicorn

from src.core.settings import get_cached_settings
from src.core.util import setup_logging


def __just_script():
    setup_logging()
    uvicorn.run(
        "src.api.asgi:app",
        port=get_cached_settings().api_port,
        host="localhost",
        workers=1,
        reload=False
    )


if __name__ == '__main__':
    __just_script()

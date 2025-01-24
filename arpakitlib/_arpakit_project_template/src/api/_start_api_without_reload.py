import uvicorn

from src.core.settings import get_cached_settings


def _start_api_for_dev_without_reload():
    uvicorn.run(
        "src.api.asgi:app",
        port=get_cached_settings().api_port,
        host="localhost",
        workers=1,
        reload=False
    )


if __name__ == '__main__':
    _start_api_for_dev_without_reload()

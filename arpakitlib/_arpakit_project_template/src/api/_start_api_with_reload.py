import uvicorn

from src.core.settings import get_cached_settings


def _start_api_for_dev_with_reload():
    uvicorn.run(
        "src.api.asgi:app",
        port=get_cached_settings().api_port,
        host="localhost",
        workers=1,
        reload=True
    )


if __name__ == '__main__':
    _start_api_for_dev_with_reload()

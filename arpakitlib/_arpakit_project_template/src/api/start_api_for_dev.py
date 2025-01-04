import uvicorn

from src.core.settings import get_cached_settings


def start_api_for_dev(*, reload: bool = False):
    uvicorn.run(
        "src.api.asgi:app",
        port=get_cached_settings().api_port,
        host="localhost",
        workers=1,
        reload=reload
    )


if __name__ == '__main__':
    start_api_for_dev(reload=False)

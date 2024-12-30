import uvicorn


def start_app_for_dev(reload: bool = True):
    uvicorn.run(
        "src.api.asgi:app",
        port=...,
        host="localhost",
        workers=1,
        reload=reload
    )


if __name__ == '__main__':
    start_app_for_dev()

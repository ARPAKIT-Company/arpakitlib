import uvicorn


def start_api_for_dev(reload: bool = True):
    uvicorn.run(
        "src.api.asgi:app",
        port=int("{API_PORT}"),
        host="localhost",
        workers=1,
        reload=reload
    )


if __name__ == '__main__':
    start_api_for_dev()

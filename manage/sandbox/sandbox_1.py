import asyncio

import uvicorn

from arpakitlib.ar_fastapi_util import create_fastapi_app, create_handle_exception, ErrorSO, \
    create_handle_exception_creating_story_log
from arpakitlib.ar_sleep_util import async_safe_sleep
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB


async def f(error_so: ErrorSO, status_code: int, **kwargs):
    print("2st4wtwetwest")
    return status_code, error_so


def command():
    sqlalchemy_db = SQLAlchemyDB(db_url="postgresql://arpakitlib:arpakitlib@localhost:50629/arpakitlib")
    sqlalchemy_db.reinit()

    app = create_fastapi_app(
        handle_exception_=create_handle_exception(
            funcs_before_response=[
                create_handle_exception_creating_story_log(sqlalchemy_db=sqlalchemy_db)
            ]
        )
    )
    uvicorn.run(app=app)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

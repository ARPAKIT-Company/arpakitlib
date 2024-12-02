import asyncio

import uvicorn

from arpakitlib.ar_easy_sqlalchemy_util import EasySQLAlchemyDB
from arpakitlib.ar_fastapi_util import create_fastapi_app, APIStartupEventInitEasySQLAlchemyDB
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_util import OperationDBM, ExecuteOperationWorker, BaseOperationExecutor


def command():
    setup_normal_logging()

    easy_sqlalchemy_db = EasySQLAlchemyDB(
        db_url="postgresql://arpakitlib:arpakitlib@127.0.0.1:50629/arpakitlib",
        need_include_operation_dbm=True,
        need_include_story_dbm=True
    )
    easy_sqlalchemy_db.reinit()

    for i in range(10):
        with easy_sqlalchemy_db.new_session() as session:
            session.add(OperationDBM(type=OperationDBM.Types.raise_fake_exception))
            session.commit()

    worker = ExecuteOperationWorker(
        easy_sql_alchemy_db=easy_sqlalchemy_db,
        operation_executor=BaseOperationExecutor(easy_sql_alchemy_db=easy_sqlalchemy_db)
    )
    worker.sync_safe_run()


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())

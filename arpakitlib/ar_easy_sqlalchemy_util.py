# arpakit

import logging
from datetime import timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy import create_engine, QueuePool, text, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class EasySQLAlchemyDB:
    def __init__(
            self,
            *,
            db_url: str,
            echo: bool = False,
            need_include_operation_dbm: bool = False,
            need_include_story_dbm: bool = False
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.need_include_operation_dbm = need_include_operation_dbm
        self.need_include_story_dbm = need_include_story_dbm
        if self.need_include_operation_dbm:
            self.need_include_story_dbm = True
        self.engine = create_engine(
            url=db_url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
            poolclass=QueuePool,
            pool_timeout=timedelta(seconds=30).total_seconds()
        )
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.func_new_session_counter = 0

    def include_operation_dbm(self):
        if self.need_include_operation_dbm:
            from arpakitlib.ar_operation_util import import_ar_operation_execution_util
            import_ar_operation_execution_util()

    def include_story_dbm(self):
        if self.need_include_story_dbm or self.need_include_operation_dbm:
            from arpakitlib.ar_story_log_util import import_ar_story_util
            import_ar_story_util()

    def drop_celery_tables(self):
        with self.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS celery_tasksetmeta CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS celery_taskmeta CASCADE;"))
            connection.commit()
            self._logger.info("celery tables were dropped")

    def remove_celery_tables_data(self):
        with self.engine.connect() as connection:
            connection.execute(text("DELETE FROM celery_tasksetmeta;"))
            connection.execute(text("DELETE FROM celery_taskmeta;"))
            connection.commit()
            self._logger.info("celery tables data were removed")

    def init(self):
        self.include_operation_dbm()
        self.include_story_dbm()
        from arpakitlib.ar_sqlalchemy_model_util import BaseDBM
        BaseDBM.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was inited")

    def drop(self):
        from arpakitlib.ar_sqlalchemy_model_util import BaseDBM
        BaseDBM.metadata.drop_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was dropped")

    def reinit(self):
        self.include_operation_dbm()
        self.include_story_dbm()
        from arpakitlib.ar_sqlalchemy_model_util import BaseDBM
        BaseDBM.metadata.drop_all(bind=self.engine, checkfirst=True)
        BaseDBM.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was reinited")

    def check_conn(self):
        self.engine.connect()
        self._logger.info("db conn is good")

    def new_session(self) -> Session:
        self.func_new_session_counter += 1
        return self.sessionmaker(bind=self.engine)

    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def generate_unique_id(self, *, class_dbm: Any):
        with self.new_session() as session:
            res: int = session.query(func.max(class_dbm.id)).scalar()
            while session.query(class_dbm).filter(class_dbm.id == res).first() is not None:
                res += 1
        return res

    def generate_unique_long_id(self, *, class_dbm: Any):
        with self.new_session() as session:
            res: str = str(uuid4())
            while session.query(class_dbm).filter(class_dbm.long_id == res).first() is not None:
                res = str(uuid4())
        return res


def __example():
    pass


if __name__ == '__main__':
    __example()

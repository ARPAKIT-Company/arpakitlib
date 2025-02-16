from src.core.util import setup_logging
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def _check_conn_sqlalchemy_db():
    setup_logging()
    get_cached_sqlalchemy_db().check_conn()


if __name__ == '__main__':
    _check_conn_sqlalchemy_db()

from src.core.util import setup_logging
from src.db.util import get_cached_sqlalchemy_db


def __check_conn_sqlalchemy_db():
    setup_logging()
    get_cached_sqlalchemy_db().check_conn()


if __name__ == '__main__':
    __check_conn_sqlalchemy_db()

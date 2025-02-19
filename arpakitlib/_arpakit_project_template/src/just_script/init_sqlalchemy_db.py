from src.core.util import setup_logging
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def __just_script():
    setup_logging()
    get_cached_sqlalchemy_db().init()


if __name__ == '__main__':
    __just_script()

from core.settings import get_cached_settings
from core.util import setup_logging
from sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    get_cached_sqlalchemy_db().drop()
    get_cached_sqlalchemy_db().drop_celery_tables()
    get_cached_sqlalchemy_db().drop_alembic_tables()


if __name__ == '__main__':
    __command()

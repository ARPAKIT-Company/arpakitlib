from src.core.settings import get_cached_settings
from src.core.util import setup_logging
from src.db.util import get_cached_sqlalchemy_db


def _reinit_sqlalchemy_db():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    get_cached_sqlalchemy_db().reinit()


if __name__ == '__main__':
    _reinit_sqlalchemy_db()

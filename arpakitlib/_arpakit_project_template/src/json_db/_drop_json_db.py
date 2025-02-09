from src.core.settings import get_cached_settings
from src.core.util import setup_logging
from src.json_db.util import get_json_db


def _init_json_db():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    get_json_db().drop()


if __name__ == '__main__':
    _init_json_db()

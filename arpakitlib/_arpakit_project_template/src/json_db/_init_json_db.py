from src.core.util import setup_logging
from src.json_db.util import get_json_db


def _init_json_db():
    setup_logging()
    get_json_db().init()


if __name__ == '__main__':
    _init_json_db()

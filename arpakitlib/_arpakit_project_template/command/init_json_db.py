from core.util import setup_logging
from json_db.util import get_json_db


def __command():
    setup_logging()
    get_json_db().init()


if __name__ == '__main__':
    __command()

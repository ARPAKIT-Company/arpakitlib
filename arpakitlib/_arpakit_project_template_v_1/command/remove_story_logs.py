from core.settings import get_cached_settings
from core.util import setup_logging
from sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


def __command():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    with get_cached_sqlalchemy_db().new_session() as session:
        session.query(StoryLogDBM).delete()
        session.commit()


if __name__ == '__main__':
    __command()

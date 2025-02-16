from src.core.settings import get_cached_settings
from src.core.util import setup_logging
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db
from src.sqlalchemy_db.sqlalchemy_model import StoryLogDBM


def _remove_story_logs():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    with get_cached_sqlalchemy_db().new_session() as session:
        session.query(StoryLogDBM).delete()
        session.commit()


if __name__ == '__main__':
    _remove_story_logs()

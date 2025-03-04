from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from project.sqlalchemy_db_.sqlalchemy_model.operation import OperationDBM
from project.sqlalchemy_db_.sqlalchemy_model.story_log import StoryLogDBM

if __name__ == '__main__':
    print(get_string_info_from_declarative_base(SimpleDBM))

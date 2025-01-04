from arpakitlib.ar_sqlalchemy_model_util import SimpleDBM
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base

# ...


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(SimpleDBM))

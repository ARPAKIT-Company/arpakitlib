from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from src.core.settings import get_cached_settings
from src.core.util import setup_logging


def __check_settings():
    setup_logging()
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))


if __name__ == '__main__':
    __check_settings()

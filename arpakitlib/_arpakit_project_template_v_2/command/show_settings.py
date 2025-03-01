from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from project.core.settings import get_cached_settings


def __command():
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))


if __name__ == '__main__':
    __command()

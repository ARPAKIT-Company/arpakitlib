import os.path

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from src.core.const import BASE_DIRPATH
from src.core.settings import Settings, get_cached_settings
from src.core.util import setup_logging


def command():
    setup_logging()
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))
    Settings.save_env_example_to_file(filepath=os.path.join(BASE_DIRPATH, "example.env"))


if __name__ == '__main__':
    command()

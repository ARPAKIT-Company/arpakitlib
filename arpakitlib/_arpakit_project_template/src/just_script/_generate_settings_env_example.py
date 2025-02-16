import os.path

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from src.core.const import ProjectPaths
from src.core.settings import Settings, get_cached_settings


def _generate_settings_env_example():
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))
    Settings.save_env_example_to_file(filepath=os.path.join(ProjectPaths.base_dirpath, "example.env"))


if __name__ == '__main__':
    _generate_settings_env_example()

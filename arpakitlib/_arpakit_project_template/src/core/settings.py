import os
from functools import lru_cache

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_settings_util import AdvancedSettings
from src.core.const import ProjectPaths


class Settings(AdvancedSettings):
    var_dirpath: str | None = os.path.join(ProjectPaths.base_dirpath, "var")


@lru_cache()
def get_cached_settings() -> Settings:
    if os.path.exists(ProjectPaths.env_filepath):
        return Settings(_env_file=ProjectPaths.env_filepath, _env_file_encoding="utf-8")
    return Settings()


if __name__ == '__main__':
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))

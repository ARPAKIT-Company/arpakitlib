import asyncio
import os
from functools import lru_cache

from arpakitlib.ar_json_util import safely_transfer_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from project_template.src.core.const import BASE_DIRPATH, ENV_FILEPATH


class Settings(SimpleSettings):
    log_filename: str = "story.log"

    log_filepath: str = os.path.join(BASE_DIRPATH, log_filename)


@lru_cache()
def get_cached_settings() -> Settings:
    if os.path.exists(ENV_FILEPATH):
        return Settings(_env_file=ENV_FILEPATH, _env_file_encoding="utf-8")
    return Settings()


def __example():
    print(safely_transfer_to_json_str(get_cached_settings().model_dump(mode="json")))


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

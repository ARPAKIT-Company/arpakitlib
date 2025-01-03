import asyncio
import os
from functools import lru_cache

from arpakitlib.ar_json_util import safely_transfer_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from src.core.const import BASE_DIRPATH, ENV_FILEPATH


class Settings(SimpleSettings):
    # ...

    var_dirname: str = "var"

    var_dirpath: str = os.path.join(BASE_DIRPATH, var_dirname)

    log_filename: str = "story.log"

    log_filepath: str = os.path.join(var_dirpath, log_filename)

    cache_dirname: str = "cache"

    cache_dirpath: str = os.path.join(var_dirpath, cache_dirname)

    media_dirname: str = "media"

    media_dirpath: str = os.path.join(var_dirpath, media_dirname)

    dump_dirname: str = "dump"

    dump_dirpath: str = os.path.join(var_dirpath, dump_dirname)

    sql_db_url: str | None = (
        "postgresql://{PROJECT_NAME}:{PROJECT_NAME}@127.0.0.1:{SQL_DB_PORT}/{PROJECT_NAME}"
    )

    init_sql_db_at_start: bool = False

    sql_db_echo: bool = False


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

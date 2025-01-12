import asyncio
import os
from functools import lru_cache
from typing import Any

import pytz

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from src.core.const import BASE_DIRPATH, ENV_FILEPATH


class Settings(SimpleSettings):
    project_name: str = "{PROJECT_NAME}"

    sql_db_url: str | None = (
        "postgresql://{PROJECT_NAME}:{PROJECT_NAME}@127.0.0.1:{SQL_DB_PORT}/{PROJECT_NAME}"
    ) if (str("{PROJECT_NAME}") and str("{SQL_DB_PORT}").strip().isdigit()) else None

    sql_db_echo: bool = False

    api_init_sql_db_at_start: bool = True

    api_title: str = "{PROJECT_NAME}"

    api_description: str = "{PROJECT_NAME} (arpakitlib)"

    api_create_story_log_before_response_in_handle_exception: bool = True

    api_start_operation_executor_worker: bool = False

    api_start_scheduled_operation_creator_worker: bool = False

    api_port: int | None = int("{API_PORT}") if "{API_PORT}".strip().isdigit() else None

    api_correct_api_key: str | None = "1"

    api_correct_token: str | None = "1"

    var_dirname: str | None = "var"

    var_dirpath: str | None = os.path.join(BASE_DIRPATH, var_dirname)

    log_filename: str | None = "story.log"

    log_filepath: str | None = os.path.join(var_dirpath, log_filename)

    cache_dirname: str | None = "cache"

    cache_dirpath: str | None = os.path.join(var_dirpath, cache_dirname)

    media_dirname: str | None = "media"

    media_dirpath: str | None = os.path.join(var_dirpath, media_dirname)

    dump_dirname: str | None = "dump"

    dump_dirpath: str | None = os.path.join(var_dirpath, dump_dirname)

    local_timezone: str | None = None

    @property
    def local_timezone_as_pytz(self) -> Any:
        return pytz.timezone(self.local_timezone)

    # ...


@lru_cache()
def get_cached_settings() -> Settings:
    if os.path.exists(ENV_FILEPATH):
        return Settings(_env_file=ENV_FILEPATH, _env_file_encoding="utf-8")
    return Settings()


def __example():
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

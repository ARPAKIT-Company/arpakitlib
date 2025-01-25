import os
from functools import lru_cache
from typing import Any

import pytz
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from src.core.const import ProjectPaths


class Settings(SimpleSettings):
    project_name: str = "{{PROJECT_NAME}}"

    sql_db_user: str | None = project_name

    sql_db_password: str | None = project_name

    sql_db_port: int | None = int("{{SQL_DB_PORT}}") if "{{SQL_DB_PORT}}".strip().isdigit() else None

    sql_db_database: str | None = project_name

    sql_db_url: str | None = None

    @field_validator("sql_db_url", mode="after")
    def validate_sql_db_url(cls, v: Any, validation_info: ValidationInfo) -> str | None:
        if v is not None:
            return None
        user = validation_info.data.get('sql_db_user')
        password = validation_info.data.get('sql_db_password')
        port = validation_info.data.get('sql_db_port')
        database = validation_info.data.get('sql_db_database')
        if user is not None and password is not None and port is not None and database is not None:
            return f"postgresql://{user}:{password}@127.0.0.1:{port}/{database}"
        return None

    sql_db_echo: bool = False

    api_init_sql_db_at_start: bool = True

    api_title: str = project_name

    api_description: str = f"{project_name} (arpakitlib)"

    api_create_story_log_before_response_in_handle_exception: bool = True

    api_start_operation_executor_worker: bool = False

    api_start_scheduled_operation_creator_worker: bool = False

    api_port: int | None = int("{{API_PORT}}") if "{{API_PORT}}".strip().isdigit() else None

    api_correct_api_key: str | None = "1"

    api_correct_token: str | None = "1"

    api_enable_admin1: bool = True

    var_dirname: str | None = "var"

    var_dirpath: str | None = os.path.join(ProjectPaths.base_dirpath, var_dirname)

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

    admin1_secret_key: str | None = "85a9583cb91c4de7a78d7eb1e5306a04418c9c43014c447ea8ec8dd5deb4cf71"

    # ...


@lru_cache()
def get_cached_settings() -> Settings:
    if os.path.exists(ProjectPaths.env_filepath):
        return Settings(_env_file=ProjectPaths.env_filepath, _env_file_encoding="utf-8")
    return Settings()


if __name__ == '__main__':
    print(safely_transfer_obj_to_json_str(get_cached_settings().model_dump(mode="json")))

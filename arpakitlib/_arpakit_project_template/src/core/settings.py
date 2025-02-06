import os
from functools import lru_cache
from typing import Any

import pytz
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from arpakitlib.ar_sqlalchemy_util import generate_sqlalchemy_url
from src.core.const import ProjectPaths


class Settings(SimpleSettings):
    project_name: str | None = "{{PROJECT_NAME}}"

    sql_db_user: str | None = project_name

    sql_db_password: str | None = project_name

    sql_db_port: int | None = int("{{SQL_DB_PORT}}") if "{{SQL_DB_PORT}}".strip().isdigit() else None

    sql_db_database: str | None = project_name

    sql_db_url: str | None = None

    @field_validator("sql_db_url", mode="after")
    def validate_sql_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        user = validation_info.data.get("sql_db_user")
        password = validation_info.data.get("sql_db_password")
        port = validation_info.data.get("sql_db_port")
        database = validation_info.data.get("sql_db_database")

        return generate_sqlalchemy_url(
            base="postgresql",
            user=user,
            password=password,
            port=port,
            database=database
        )

    async_sql_db_url: str | None = None

    @field_validator("async_sql_db_url", mode="after")
    def validate_async_sql_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        user = validation_info.data.get("sql_db_user")
        password = validation_info.data.get("sql_db_password")
        port = validation_info.data.get("sql_db_port")
        database = validation_info.data.get("sql_db_database")

        return generate_sqlalchemy_url(
            base="postgresql+asyncpg",
            user=user,
            password=password,
            port=port,
            database=database
        )

    sql_db_echo: bool = False

    api_init_sql_db_at_start: bool = True

    api_title: str | None = project_name

    api_description: str | None = f"{project_name} (arpakitlib)"

    api_logging_func_before_response: bool = True

    api_story_log_func_before_response: bool = True

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

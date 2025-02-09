# arpakit
import os
from typing import Union, Any

import pytz
from pydantic import ConfigDict, field_validator, model_validator
from pydantic_core import PydanticUndefined
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from arpakitlib.ar_sqlalchemy_util import generate_sqlalchemy_url

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_env_example(settings_class: Union[BaseSettings, type[BaseSettings]]):
    res = ""
    for k, f in settings_class.model_fields.items():
        if f.default is not PydanticUndefined:
            res += f"# {k}=\n"
        else:
            res += f"{k}=\n"
    return res


class ModeTypes(Enumeration):
    not_prod: str = "not_prod"
    prod: str = "prod"


class BaseSettings2(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def validate_all_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        for key, value in values.items():
            if isinstance(value, str) and value.lower().strip() in {"null", "none", "nil"}:
                values[key] = None
        return values

    @classmethod
    def generate_env_example(cls) -> str:
        return generate_env_example(settings_class=cls)

    @classmethod
    def save_env_example_to_file(cls, filepath: str) -> str:
        env_example = cls.generate_env_example()
        with open(filepath, mode="w") as f:
            f.write(env_example)
        return env_example


class SimpleSettings(BaseSettings2):
    mode_type: str = ModeTypes.not_prod

    @field_validator("mode_type")
    @classmethod
    def validate_mode_type(cls, v: str):
        ModeTypes.parse_and_validate_values(v.lower().strip())
        return v

    @property
    def is_mode_type_not_prod(self) -> bool:
        return self.mode_type == ModeTypes.not_prod

    def raise_if_mode_type_not_prod(self):
        if self.is_mode_type_not_prod:
            raise ValueError(f"mode type = {self.mode_type}")

    @property
    def is_mode_type_prod(self) -> bool:
        return self.mode_type == ModeTypes.prod

    def raise_if_mode_type_prod(self):
        if self.is_mode_type_prod:
            raise ValueError(f"mode type = {self.mode_type}")


class AdvancedSettings(SimpleSettings):
    project_name: str | None = None

    sql_db_user: str | None = None

    @field_validator("sql_db_user", mode="after")
    def validate_sql_db_user(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        res = validation_info.data.get("project_name")
        if res is not None:
            return res
        return res

    sql_db_password: str | None = None

    @field_validator("sql_db_password", mode="after")
    def validate_sql_db_password(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        res = validation_info.data.get("project_name")
        if res is not None:
            return res
        return res

    sql_db_port: int | None = int("50506") if "50506".strip().isdigit() else None

    sql_db_database: str | None = None

    @field_validator("sql_db_database", mode="after")
    def validate_sql_db_database(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        res = validation_info.data.get("project_name")
        if res is not None:
            return res
        return res

    sync_sql_db_url: str | None = None

    @field_validator("sync_sql_db_url", mode="after")
    def validate_sync_sql_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        return generate_sqlalchemy_url(
            base="postgresql",
            user=validation_info.data.get("sql_db_user"),
            password=validation_info.data.get("sql_db_password"),
            port=validation_info.data.get("sql_db_port"),
            database=validation_info.data.get("sql_db_database")
        )

    async_sql_db_url: str | None = None

    @field_validator("async_sql_db_url", mode="after")
    def validate_async_sql_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        return generate_sqlalchemy_url(
            base="postgresql+asyncpg",
            user=validation_info.data.get("sql_db_user"),
            password=validation_info.data.get("sql_db_password"),
            port=validation_info.data.get("sql_db_port"),
            database=validation_info.data.get("sql_db_database")
        )

    sql_db_echo: bool = False

    api_port: int | None = None

    @field_validator("api_port", mode="before")
    def validate_api_port(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> int | None:
        if isinstance(v, str):
            if v.isdigit():
                return int(v)
        return None

    api_init_sql_db_at_start: bool = True

    api_logging__api_func_before_in_handle_exception: bool = True

    api_story_log__api_func_before_in_handle_exception: bool = True

    api_correct_api_key: str | None = "1"

    api_correct_token: str | None = "1"

    api_enable_admin1: bool = True

    admin1_secret_key: str | None = "85a9583cb91c4de7a78d7eb1e5306a04418c9c43014c447ea8ec8dd5deb4cf71"

    var_dirpath: str | None = "./var"

    log_filepath: str | None = None

    @field_validator("log_filepath", mode="after")
    def validate_log_filepath(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        var_dirpath = validation_info.data.get("var_dirpath")
        if var_dirpath is None:
            return None
        return os.path.join(var_dirpath, "story.log")

    cache_dirpath: str | None = None

    @field_validator("cache_dirpath", mode="after")
    def validate_cache_dirpath(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        var_dirpath = validation_info.data.get("var_dirpath")
        if var_dirpath is None:
            return None
        return os.path.join(var_dirpath, "cache")

    media_dirpath: str | None = None

    @field_validator("media_dirpath", mode="after")
    def validate_media_dirpath(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        var_dirpath = validation_info.data.get("var_dirpath")
        if var_dirpath is None:
            return None
        return os.path.join(var_dirpath, "media")

    dump_dirpath: str | None = None

    @field_validator("dump_dirpath", mode="after")
    def validate_dump_dirpath(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        var_dirpath = validation_info.data.get("var_dirpath")
        if var_dirpath is None:
            return None
        return os.path.join(var_dirpath, "dump")

    local_timezone: str | None = None

    @property
    def local_timezone_as_pytz(self) -> Any:
        return pytz.timezone(self.local_timezone)

    json_db_dirpath: str | None = None

    @field_validator("json_db_dirpath", mode="after")
    def validate_json_db_dirpath(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v
        var_dirpath = validation_info.data.get("var_dirpath")
        if var_dirpath is None:
            return None
        project_name = validation_info.data.get("project_name")
        return os.path.join(var_dirpath, f"{project_name}_json_db")


def __example():
    print(safely_transfer_obj_to_json_str(AdvancedSettings(var_dirpath="./var").model_dump(mode="json")))


if __name__ == '__main__':
    __example()

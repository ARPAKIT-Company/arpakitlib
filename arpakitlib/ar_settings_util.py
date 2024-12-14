from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_generate_env_example import generate_env_example


class SimpleSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    class ModeTypes(Enumeration):
        local: str = "local"
        test: str = "preprod"
        prod: str = "prod"

    mode_type: str = ModeTypes.local

    @field_validator("mode_type")
    @classmethod
    def validate_mode_type(cls, v: str):
        cls.ModeTypes.parse_and_validate_values(v)
        return v

    @property
    def is_mode_type_local(self) -> bool:
        return self.mode_type == self.ModeTypes.local

    @property
    def is_mode_type_test(self) -> bool:
        return self.mode_type == self.ModeTypes.test

    @property
    def is_mode_type_prod(self) -> bool:
        return self.mode_type == self.ModeTypes.prod

    @classmethod
    def env_example(cls) -> str:
        return generate_env_example(settings_class=cls)

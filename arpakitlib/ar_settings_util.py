# arpakit

from typing import Union

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

from arpakitlib.ar_enumeration_util import Enumeration


def generate_env_example(settings_class: Union[BaseSettings, type[BaseSettings]]):
    res = ""
    for k, f in settings_class.model_fields.items():
        if f.default:
            res += f"# {k}=\n"
        else:
            res += f"{k}=\n"
    return res


class SimpleSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    class ModeTypes(Enumeration):
        dev: str = "dev"
        prod: str = "prod"

    mode_type: str = ModeTypes.dev

    @field_validator("mode_type")
    @classmethod
    def validate_mode_type(cls, v: str):
        cls.ModeTypes.parse_and_validate_values(v)
        return v

    @property
    def is_mode_type_dev(self) -> bool:
        return self.mode_type == self.ModeTypes.dev

    @property
    def is_mode_type_prod(self) -> bool:
        return self.mode_type == self.ModeTypes.prod

    @classmethod
    def generate_env_example(cls) -> str:
        return generate_env_example(settings_class=cls)


def __example():
    default_settings = SimpleSettings()
    print(f"Настройки по умолчанию: {default_settings.mode_type}")

    if default_settings.is_mode_type_dev:
        print("Приложение запущено в режиме разработки")
    elif default_settings.is_mode_type_prod:
        print("Приложение запущено в режиме продакшена")

    said_settings = SimpleSettings(mode_type="prod")
    print(f"\nУказанные настройки: {said_settings.mode_type}")

    if said_settings.is_mode_type_dev:
        print("Приложение запущено в режиме разработки")
    elif said_settings.is_mode_type_prod:
        print("Приложение запущено в режиме продакшена")

    # Неверное значение для mode_type
    try:
        SimpleSettings(mode_type="invalid_value")
    except Exception as e:
        print(f"\nОшибка: {e}")

    # Генерация конфигурации
    print("\nГенерация примера конфигурации:")
    print(SimpleSettings.generate_env_example())


if __name__ == '__main__':
    __example()

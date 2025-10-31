# arpakit
import ast
import asyncio
import logging
from typing import Any, get_origin, get_args

from aiogram import types
from aiogram.filters import CommandObject
from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import PydanticUndefined

from arpakitlib.ar_parse_command_util import parse_command
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class BaseTgCommandModel(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)

    desc: str | None = Field(default=None)
    help: bool = Field(default=False)


class ExampleTgCommandModel(BaseTgCommandModel):
    hello: str | None = Field(description="Example Desc", default="Hello world")


def _generate_help_text(command_name: str, model_class: type[BaseTgCommandModel]) -> str:
    """Генерирует help-текст по описанию модели."""
    lines = [f"<b>Command</b> /{command_name}"]

    desc_field = model_class.model_fields.get("desc")

    if desc_field:
        if desc_field.default:
            raise_for_type(desc_field.default, str)
            lines.append(f"\n\n{desc_field.default}")

    lines.append(f"\n\n<b>Fields ({len(model_class.model_fields.items())}):</b>")

    for name, field in model_class.model_fields.items():
        if name in ("desc",):
            continue

        default_value = (
            field.default
            if field.default is not PydanticUndefined
            else "<i>required</i>"
        )

        origin = get_origin(field.annotation)
        args = get_args(field.annotation)

        if origin is list and args:
            type_name = f"list[{args[0].__name__}]"
        elif hasattr(field.annotation, "__name__"):
            type_name = field.annotation.__name__
        else:
            type_name = str(field.annotation)

        desc = f" — {field.description}" if field.description else ""

        lines.append(f"\n• <code>-{name}</code>: <i>{type_name}</i>{desc} (default: {default_value})")

    lines.append(f"\n\n<b>Usage for help:</b>\n<code>/{command_name} -help</code>")

    return "\n".join(lines)


def _smart_parse_tg_command_param(value: Any) -> Any:
    """Интеллектуальное преобразование строки из Telegram-команды в Python-значение."""
    if isinstance(value, (bool, int, float)) or value is None:
        return value

    v = value.strip()
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"

    try:
        result = ast.literal_eval(v)
        # Если получился список — проверим, не смесь ли типов
        if isinstance(result, list):
            # Если все элементы одного типа — оставляем
            if len(result) > 0 and len({type(x) for x in result}) > 1:
                # Приводим всё к строкам для единообразия
                result = [str(x) for x in result]
        return result
    except Exception:
        # не получилось распарсить — возвращаем как строку
        return v


def as_tg_command_handler(
        *,
        tg_command_format_class: type[BaseTgCommandModel]
):
    def decorator(handler):

        async def new_handler(*args, **kwargs):

            message: types.Message = args[0]
            if not isinstance(message, types.Message):
                raise TypeError("not isinstance(message, types.Message)")

            tg_command: CommandObject = kwargs["command"]

            try:

                parsed_command = parse_command(text=tg_command.text)
                kwargs["parsed_command"] = parsed_command

                if parsed_command.has_flag(flag="help") or parsed_command.has_flag(flag="h"):
                    help_text = _generate_help_text(
                        command_name=tg_command.command,
                        model_class=tg_command_format_class,
                    )
                    await message.answer(text=help_text, disable_web_page_preview=True)
                    return None

                tg_command_model_data: dict[str, Any] = {}
                for key, value in parsed_command.key_to_value.items():
                    if value is None:
                        tg_command_model_data[key] = True
                    else:
                        tg_command_model_data[key] = _smart_parse_tg_command_param(value=value)

                # позиционные аргументы (если нужны)
                for i, value in enumerate(parsed_command.values_without_key):
                    tg_command_model_data[f"arg_{i}"] = _smart_parse_tg_command_param(value=value)

                tg_command_format_obj = tg_command_format_class(**tg_command_model_data)

            except Exception as exception:

                _logger.error(f"error in {tg_command.text}", exc_info=True)

                await message.answer(
                    text=(
                        f"<b>Bad command usage</b> /{tg_command.command}"
                        f"\n"
                        f"\n<b>Error:</b>"
                        f"\n{exception}"
                        f"\n"
                        f"\nUse <code>/{tg_command.command} -help</code> for help info"
                    ),
                    disable_web_page_preview=True,
                )

                return None

            kwargs["tg_command_format_obj"] = tg_command_format_obj

            return await handler(*args, **kwargs)

        return new_handler

    return decorator


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())

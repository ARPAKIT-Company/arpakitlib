# arpakit
import datetime as dt
from typing import Any, Optional, get_type_hints

from pydantic import BaseModel, Field
from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql.sqltypes import (
    Boolean, Integer, BigInteger, SmallInteger,
    String, Text, Unicode, UnicodeText,
    DateTime, Date, Time,
    Float, Numeric, DECIMAL, LargeBinary, JSON
)

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_SQLA_TYPE_MAP = {
    Boolean: bool,
    Integer: int,
    BigInteger: int,
    SmallInteger: int,
    Float: float,
    Numeric: float,
    DECIMAL: float,
    String: str,
    Unicode: str,
    Text: str,
    UnicodeText: str,
    LargeBinary: bytes,
    JSON: dict,
    DateTime: dt.datetime,
    Date: dt.date,
    Time: dt.time,
}


def _python_type_from_col(col) -> type | str:
    try:
        return col.type.python_type
    except Exception:
        for sa_t, py_t in _SQLA_TYPE_MAP.items():
            if isinstance(col.type, sa_t):
                return py_t
        return Any


def _get_property_name_to_type_from_model_class(model_class: type) -> dict[str, Any]:
    """
    Находит все @property в классе и вытаскивает их возвращаемый тип.
    Если тип не удаётся получить — подставляем Any.
    """
    props: dict[str, Any] = {}
    for name, attr in vars(model_class).items():
        if isinstance(attr, property):
            try:
                hints = get_type_hints(attr.fget) if attr.fget else {}
                ret_type = hints.get("return", Any)
            except Exception:
                ret_type = Any
            props[name] = ret_type
    return props


def pydantic_schema_from_sqlalchemy_model(
        sqlalchemy_model: type,
        *,
        model_name: str | None = None,
        base_model: type[BaseModel] = BaseModel,
        include_column_defaults: bool = False,
        exclude_column_names: list[str] | None = None,
        include_properties: bool = False,
        include_property_names: list[str] | None = None,
        exclude_property_names: list[str] | None = None,
        filter_property_prefixes: list[str] | None = None,
        remove_prefixes: list[str] | None = None,
) -> type[BaseModel]:
    """
    Генерирует Pydantic-модель из колонок SQLAlchemy-модели и (опционально) из @property.

    - include_column_defaults: добавлять ли default/server_default у колонок.
    - exclude_column_names: список имён колонок, которые нужно пропустить.

    - include_properties: включать ли свойства (@property). По умолчанию False.
    - include_property_names: whitelist имён свойств (если задан, берём только их).
    - exclude_property_names: blacklist имён свойств (исключаются после whitelist'а).
    """
    mapper = inspect(sqlalchemy_model).mapper
    model_name = model_name or f"{sqlalchemy_model.__name__}Schema"

    annotations: dict[str, Any] = {}
    attrs: dict[str, Any] = {}

    exclude_column_names = set(set(exclude_column_names) or [])
    include_property_names = set(set(include_property_names) or [])
    exclude_property_names = set(set(exclude_property_names) or [])
    filter_property_prefixes = list(set(filter_property_prefixes) or [])
    remove_prefixes = list(set(remove_prefixes) or [])

    # 1) Колонки
    for prop in mapper.attrs:
        if not isinstance(prop, ColumnProperty):
            continue
        if prop.key in exclude_column_names:
            continue

        column = prop.columns[0]
        column_type = _python_type_from_col(column)

        # Аннотация типа
        if column.nullable:
            annotations[prop.key] = Optional[column_type]  # type: ignore[name-defined]
        else:
            annotations[prop.key] = column_type

        # Дефолты, если нужно
        if include_column_defaults:
            default_value = None
            if column.default is not None and getattr(column.default, "is_scalar", False):
                default_value = column.default.arg
            elif column.server_default is not None and getattr(column.server_default.arg, "text", None):
                default_value = column.server_default.arg.text

            if default_value is not None:
                attrs[prop.key] = Field(default=default_value)

    # 2) Свойства (@property)
    if include_properties:
        property_name_to_type = _get_property_name_to_type_from_model_class(sqlalchemy_model)

        # фильтр по префиксам (если задан и не пуст)
        if filter_property_prefixes:
            property_name_to_type = {
                property_name: property_type
                for property_name, property_type in property_name_to_type.items()
                if any(property_name.startswith(v) for v in filter_property_prefixes)
            }

        # whitelist по именам
        if include_property_names:
            property_name_to_type = {
                k: v
                for k, v in property_name_to_type.items()
                if k in include_property_names
            }
        else:
            property_name_to_type = dict(property_name_to_type)

        # blacklist по именам
        if exclude_property_names:
            for property_name in list(property_name_to_type.keys()):
                if property_name in exclude_property_names:
                    property_name_to_type.pop(property_name, None)

        # удаляем префиксы
        if remove_prefixes:
            renamed_property_name_to_type = {}
            for property_name, property_type in property_name_to_type.items():
                new_property_name = property_name
                for prefix in remove_prefixes:
                    if new_property_name.startswith(prefix):
                        new_property_name = new_property_name[len(prefix):].strip()
                        break
                if new_property_name != property_name:
                    property_name_to_type.pop(property_name)
                    # избегаем коллизий
                    if (
                            new_property_name not in annotations
                            and new_property_name not in property_name_to_type
                            and new_property_name not in renamed_property_name_to_type
                    ):
                        renamed_property_name_to_type[new_property_name] = property_type
                    else:
                        raise ValueError(
                            f"Property name '{property_name}' after removing prefix "
                            f"conflicts with existing name '{new_property_name}'"
                        )
            property_name_to_type.update(renamed_property_name_to_type)

        # добавляем (колонки в приоритете)
        for property_name, property_type in property_name_to_type.items():
            if property_name in annotations:
                continue
            annotations[property_name] = property_type

    attrs["__annotations__"] = annotations
    return type(model_name, (base_model,), attrs)

# arpakit

from typing import Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def combine_dicts(*dicts: dict) -> dict[Any, Any]:
    res = {}
    for dict_ in dicts:
        res.update(dict_)
    return res


def replace_dict_key(*, dict_: dict, old_key: Any, new_key: Any) -> dict[Any, Any]:
    if old_key in dict_:
        dict_[new_key] = dict_.pop(old_key)
    return dict_


def get_typed_from_dict(
        *,
        d: dict,
        key: str,
        type_,
        allow_unexisting: bool = False
) -> Any:
    """
    Получает d[key], проверяет, что оно относится к типу typ.
    Если ключ отсутствует:
        - если allow_non_existing=True → возвращаем None
        - иначе → KeyError
    Если тип не совпадает → TypeError
    """

    if key not in d:
        if allow_unexisting:
            return None
        raise KeyError(f"Missing key: {key}")

    val = d[key]

    if not isinstance(val, type_):
        raise TypeError(f"Expected {type_}, got {type(val)} for key '{key}'")

    return val


def __example():
    pass


if __name__ == '__main__':
    __example()

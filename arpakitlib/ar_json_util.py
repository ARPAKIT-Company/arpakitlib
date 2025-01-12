# arpakit

import json
from typing import Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def safely_transfer_str_to_json_obj(data: str) -> dict[Any, Any] | list[Any] | None:
    if not isinstance(data, str):
        raise ValueError("not isinstance(data, str)")
    return json.loads(data)


def safely_transfer_obj_to_json_str(data: dict[Any, Any] | list[Any] | None) -> str:
    if not isinstance(data, dict) and not isinstance(data, list) and data is not None:
        raise ValueError("not isinstance(data, dict) and not isinstance(data, list) and data is not None")
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def safely_transfer_obj_to_json_str_to_json_obj(
        data: dict[Any, Any] | list[Any] | None
) -> dict[Any, Any] | list[Any] | None:
    return safely_transfer_str_to_json_obj(safely_transfer_obj_to_json_str(data))


def safely_transfer_str_to_json_obj_to_json_str(data: str) -> str:
    return safely_transfer_obj_to_json_str(safely_transfer_str_to_json_obj(data))


def __example():
    pass


if __name__ == '__main__':
    __example()

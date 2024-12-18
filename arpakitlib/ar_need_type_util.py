# arpakit

import json
from typing import Any

from arpakitlib.ar_enumeration_util import Enumeration

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class NeedTypes(Enumeration):
    str_ = "str"
    int_ = "int"
    bool_ = "bool"
    float_ = "float"
    list_of_int = "list_of_int"
    list_of_str = "list_of_str"
    list_of_float = "list_of_float"
    json = "json"


def parse_need_type(value: Any, need_type: str) -> Any:
    NeedTypes.parse_and_validate_values(need_type)

    if need_type == NeedTypes.str_:
        res = value
    elif need_type == NeedTypes.int_:
        res = int(value)
    elif need_type == NeedTypes.bool_:
        if value.lower() in ["true", "1"]:
            res = True
        elif value.lower() in ["false", "0"]:
            res = False
        else:
            raise ValueError(f"value {value} is not bool type")
    elif need_type == NeedTypes.float_:
        res = float(value)
    elif need_type == NeedTypes.list_of_int:
        res = value.removeprefix("[").removesuffix("]")
        res = [int(num.strip()) for num in res.split(",")]
    elif need_type == NeedTypes.list_of_str:
        res = value.removeprefix("[").removesuffix("]")
        res = [num.strip() for num in res.split(",")]
    elif need_type == NeedTypes.list_of_float:
        res = value.removeprefix("[").removesuffix("]")
        res = [float(num.strip()) for num in res.split(",")]
    elif need_type == NeedTypes.json:
        res = json.loads(value)
    else:
        raise ValueError(f"bad need_type {need_type}")

    return res


def __example():
    pass


if __name__ == '__main__':
    __example()

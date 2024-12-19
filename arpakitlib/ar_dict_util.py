# arpakit

from typing import Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def combine_dicts(*dicts: dict) -> dict:
    res = {}
    for dict_ in dicts:
        res.update(dict_)
    return res


def replace_dict_key(*, dict_: dict, old_key: Any, new_key: Any):
    if old_key in dict_:
        dict_[new_key] = dict_.pop(old_key)
    return dict_


def __example():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    print("combine_dicts:", combine_dicts(dict1, dict2))

    dict3 = {"key1": "value1", "key2": "value2"}
    print("replace_dict_key:", replace_dict_key(dict_=dict3, old_key="key1", new_key="new_key1"))


if __name__ == '__main__':
    __example()

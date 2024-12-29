# arpakit

from typing import Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def iter_group_list(list_: list[Any], n: int):
    part = []
    for v in list_:
        if len(part) < n:
            part.append(v)
        else:
            yield part.copy()
            part = [v]
    yield part


def group_list(list_: list[Any], n: int):
    return list(iter_group_list(list_=list_, n=n))


def __example():
    data = [1, 2, 3, 4, 5, 6, 7]
    group_size = 3

    grouped_data = group_list(list_=data, n=group_size)
    print(f"Grouped data: {grouped_data}")


if __name__ == '__main__':
    __example()

# arpakit

import ipaddress

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def is_ipv4_address(value: str) -> bool:
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv4_address(value: str):
    if not is_ipv4_address(value):
        raise ValueError(f"not is_ipv4_address({value})")


def is_ipv6_address(value: str) -> bool:
    try:
        ipaddress.IPv6Address(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv6_address(value: str):
    if not is_ipv6_address(value):
        raise ValueError(f"not is_ipv6_address({value})")


def is_ipv4_interface(value: str) -> bool:
    try:
        ipaddress.IPv4Interface(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv4_interface(value: str):
    if not is_ipv4_interface(value):
        raise ValueError(f"not is_ipv4_interface({value})")


def __example():
    # ipv4
    print(is_ipv4_address("192.168.1.1"))
    try:
        raise_if_not_ipv4_address("invalid_ip")
    except ValueError as e:
        print(e)

    #ipv6
    print(is_ipv6_address("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))
    try:
        raise_if_not_ipv6_address("invalid_ip")
    except ValueError as e:
        print(e)

    # ipv4_interface
    print(is_ipv4_interface("192.168.1.1/24"))
    try:
        raise_if_not_ipv4_interface("invalid_ip")
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    __example()

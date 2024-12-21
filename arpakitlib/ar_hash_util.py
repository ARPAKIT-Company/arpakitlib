# arpakit

import hashlib

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


def check_string_hash(string: str, string_hash: str) -> bool:
    return hash_string(string) == string_hash


def __example():
    test_string = "Hello world"
    hashed_value = hash_string(string=test_string)
    print(f"hash for string '{test_string}': {hashed_value}")

    print("\nChecking hash and string for consistency")
    print("Successful") if check_string_hash(string=test_string, string_hash=hashed_value) else print("Error")



if __name__ == '__main__':
    __example()

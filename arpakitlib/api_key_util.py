from uuid import uuid4

from arpakitlib.ar_datetime_util import now_utc_dt

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_api_key() -> str:
    return (
        f"apikey{str(uuid4()).replace('-', '')}{str(now_utc_dt().timestamp()).replace('.', '')}"
    )


def __example():
    for i in range(5):
        api_key = generate_api_key()
        print(f"API-key: {api_key}")


if __name__ == '__main__':
    __example()

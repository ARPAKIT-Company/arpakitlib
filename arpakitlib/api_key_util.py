from uuid import uuid4

from arpakitlib.ar_datetime_util import now_utc_dt


def generate_default_api_key_value() -> str:
    return (
        f"apikey{str(uuid4()).replace('-', '')}{str(now_utc_dt().timestamp()).replace('.', '')}"
    )

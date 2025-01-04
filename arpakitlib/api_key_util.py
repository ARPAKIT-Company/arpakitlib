from uuid import uuid4

from arpakitlib.ar_datetime_util import now_utc_dt


def generate_api_key() -> str:
    return (
        f"apikey{str(uuid4()).replace('-', '')}{str(now_utc_dt().timestamp()).replace('.', '')}"
    )

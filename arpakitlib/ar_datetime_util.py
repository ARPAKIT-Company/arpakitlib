# arpakit

from datetime import datetime, date

import pytz

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def convert_dt_tz(dt: datetime, tz_info):
    return dt.astimezone(tz_info)


def convert_dt_tz_to_utc(dt: datetime):
    return convert_dt_tz(dt=dt, tz_info=pytz.UTC)


def now_utc_dt() -> datetime:
    return datetime.now(tz=pytz.UTC)


def now_dt(tz=pytz.UTC) -> datetime:
    return datetime.now(tz=tz)


def birth_date_to_age(*, birth_date: date, raise_if_age_negative: bool = False) -> int:
    raise_for_type(birth_date, date)
    now_utc_dt_date = now_utc_dt().date()
    res = now_utc_dt_date.year - birth_date.year
    if (now_utc_dt_date.month, now_utc_dt_date.day) < (birth_date.month, birth_date.day):
        res -= 1
    if raise_if_age_negative and res < 0:
        raise ValueError("raise_if_negative and res < 0")
    return res


def __example():
    converted = convert_dt_tz(dt=datetime.now(), tz_info=pytz.timezone("Asia/Yekaterinburg"))
    print("convert_dt_tz:", converted)

    converted_to_utc = convert_dt_tz_to_utc(dt=datetime.now())
    print("convert_dt_tz_to_utc:", converted_to_utc)

    print("now_utc_dt:", now_utc_dt())

    current_local = now_dt(pytz.timezone("Asia/Yekaterinburg"))
    print("now_dt Asia/Yekaterinburg:", current_local)

    birth_date = date(year=2002, month=1, day=25)
    age = birth_date_to_age(birth_date=birth_date)
    print("birth_date_to_age:", age)

    future_birth_date = date(year=3000, month=1, day=25)
    try:
        birth_date_to_age(birth_date=future_birth_date, raise_if_age_negative=True)
    except ValueError as e:
        print("birth_date_to_age (future date):", e)


if __name__ == '__main__':
    __example()

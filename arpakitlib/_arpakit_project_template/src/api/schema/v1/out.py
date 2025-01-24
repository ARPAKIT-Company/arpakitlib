from arpakitlib.ar_fastapi_util import BaseSO


class APIErrorInfoSO(BaseSO):
    api_error_codes: list[str] = []
    api_error_specification_codes: list[str] = []

# ...

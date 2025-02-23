from typing import Any

from api.schema.base_schema import BaseSO


class BaseCommonSO(BaseSO):
    pass


class ErrorCommonSO(BaseCommonSO):
    has_error: bool = True
    error_code: str | None = None
    error_specification_code: str | None = None
    error_description: str | None = None
    error_data: dict[str, Any] = {}

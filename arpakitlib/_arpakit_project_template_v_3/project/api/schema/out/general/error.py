from typing import Any

from project.api.schema.common import BaseSO


class ErrorGeneralSO(BaseSO):
    has_error: bool = True
    error_code: str | None = None
    error_specification_code: str | None = None
    error_description: str | None = None
    error_data: dict[str, Any] = {}

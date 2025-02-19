from typing import Any

import fastapi.security
import starlette.status

from src.api.const import APIErrorCodes
from src.api.schema.v1.out import ErrorSO


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = starlette.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = APIErrorCodes.unknown_error,
            error_specification_code: str | None = None,
            error_description: str | None = None,
            error_data: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_specification_code = error_specification_code
        self.error_description = error_description
        if error_data is None:
            error_data = {}
        self.error_data = error_data

        self.error_so = ErrorSO(
            has_error=True,
            error_code=self.error_code,
            error_specification_code=self.error_specification_code,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.error_so.model_dump(mode="json")
        )

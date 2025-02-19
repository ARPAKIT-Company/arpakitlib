import fastapi.security
import starlette.status

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str_to_json_obj
from src.api.schema.v1.out import BaseSO


class APIJSONResponse(fastapi.responses.JSONResponse):
    def __init__(self, *, content: dict | list | BaseSO | None, status_code: int = starlette.status.HTTP_200_OK):
        if isinstance(content, dict):
            content = safely_transfer_obj_to_json_str_to_json_obj(content)
        elif isinstance(content, list):
            content = safely_transfer_obj_to_json_str_to_json_obj(content)
        elif isinstance(content, BaseSO):
            content = safely_transfer_obj_to_json_str_to_json_obj(content.model_dump())
        elif content is None:
            content = None
        else:
            raise ValueError(f"unknown content type, type(content)={type(content)}")

        self.content_ = content
        self.status_code_ = status_code

        super().__init__(
            content=content,
            status_code=status_code
        )

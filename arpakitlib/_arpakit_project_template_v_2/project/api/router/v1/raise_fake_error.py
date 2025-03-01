import fastapi
import starlette.exceptions
from fastapi import APIRouter, Depends

from project.api.auth import APIAuthData, api_auth, correct_api_keys_from_settings__validate_api_key_func
from project.api.schema.common.out import ErrorCommonSO

api_router = APIRouter()


@api_router.get(
    "",
    name="Raise fake error",
    response_model=ErrorCommonSO,
    status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        n: int | None = None,
        api_auth_data: APIAuthData = Depends(api_auth(
            require_api_key_string=True,
            require_token_string=False,
            validate_api_key_func=correct_api_keys_from_settings__validate_api_key_func(),
            validate_token_func=None,
            require_correct_api_key=True,
            require_correct_token=False,
        ))
):
    if n == 1:
        raise fastapi.HTTPException(
            detail={"n": n},
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    elif n == 2:
        raise starlette.exceptions.HTTPException(
            detail=f"fake_error, n={n}",
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    elif n == 3:
        raise ValueError(f"fake error n={n}")
    else:
        raise Exception(f"fake error, n={n}")

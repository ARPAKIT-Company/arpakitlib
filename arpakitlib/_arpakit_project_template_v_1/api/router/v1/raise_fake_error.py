import fastapi
import starlette.exceptions
from fastapi import APIRouter

from api.schema.common.out import ErrorCommonSO

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
        n: int | None = None
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

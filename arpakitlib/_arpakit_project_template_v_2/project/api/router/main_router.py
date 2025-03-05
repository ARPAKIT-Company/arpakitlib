from fastapi import APIRouter

from project.api.router.general.main_router import main_general_api_router

main_api_router = APIRouter()

main_api_router.include_router(
    prefix="/general",
    router=main_general_api_router,
    tags=["General"]
)

import logging

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.core.settings import get_cached_settings


class AdminAuth(AuthenticationBackend):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(secret_key=get_cached_settings().admin1_secret_key)

    async def login(self, request: Request) -> bool:
        # ...
        # form = await request.form()
        # request.session.update(...)
        # ...
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # ...
        # request.session.get("...")
        # ...
        return True

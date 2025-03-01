import logging

import fastapi
from sqladmin.authentication import AuthenticationBackend

from project.core.settings import get_cached_settings


class SQLAdminAuth(AuthenticationBackend):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(secret_key=get_cached_settings().sqladmin_secret_key)

    async def login(self, request: fastapi.Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        if username:
            username = username.strip()
        if password:
            password = password.strip()

        if get_cached_settings().sqladmin_correct_passwords is None:
            return False
        if (
                (username is not None and username in get_cached_settings().sqladmin_correct_passwords)
                or
                (password is not None and password in get_cached_settings().sqladmin_correct_passwords)
        ):
            return True

        return False

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        if username:
            username = username.strip()
        if password:
            password = password.strip()

        if get_cached_settings().sqladmin_correct_passwords is None:
            return False
        if (
                (username is not None and username in get_cached_settings().sqladmin_correct_passwords)
                or
                (password is not None and password in get_cached_settings().sqladmin_correct_passwords)
        ):
            return True

        return False

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

        if get_cached_settings().sqladmin_correct_passwords is not None:
            if (
                    (
                            is_username_correct := (
                                    username is not None
                                    and username in get_cached_settings().sqladmin_correct_passwords
                            )
                    )
                    or
                    (
                            is_password_correct := (
                                    password is not None
                                    and password in get_cached_settings().sqladmin_correct_passwords
                            )
                    )
            ):
                if is_username_correct is True:
                    request.session.update({"sqladmin_key": username})
                elif is_password_correct is True:
                    request.session.update({"sqladmin_key": password})

                return True

        return False

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request) -> bool:
        sqladmin_key = request.session.get("sqladmin_key")
        if sqladmin_key:
            sqladmin_key = sqladmin_key.strip()

        if get_cached_settings().sqladmin_correct_passwords is not None:
            if sqladmin_key is not None and sqladmin_key in get_cached_settings().sqladmin_correct_passwords:
                return True

        return False

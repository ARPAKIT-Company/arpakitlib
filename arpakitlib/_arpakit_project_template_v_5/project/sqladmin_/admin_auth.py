import logging

import fastapi
from sqladmin.authentication import AuthenticationBackend

from arpakitlib.ar_str_util import make_none_if_blank
from project.core.settings import get_cached_settings


class SQLAdminAuth(AuthenticationBackend):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(secret_key=get_cached_settings().sqladmin_secret_key)

    async def login(self, request: fastapi.Request) -> bool:
        form = await request.form()

        username = form.get("username")
        if username:
            username = username.strip()
        username = make_none_if_blank(username)

        password = form.get("password")
        if password:
            password = password.strip()
        password = make_none_if_blank(password)

        if get_cached_settings().sqladmin_auth_keys is not None:
            if (
                    (
                            is_username_correct := (
                                    username is not None
                                    and username in get_cached_settings().sqladmin_auth_keys
                            )
                    )
                    or
                    (
                            is_password_correct := (
                                    password is not None
                                    and password in get_cached_settings().sqladmin_auth_keys
                            )
                    )
            ):
                if is_username_correct is True:
                    request.session.update({"sqladmin_auth_key": username})
                elif is_password_correct is True:
                    request.session.update({"sqladmin_auth_key": password})
                return True

        return False

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request) -> bool:
        sqladmin_auth_key = request.session.get("sqladmin_auth_key")
        if sqladmin_auth_key:
            sqladmin_auth_key = sqladmin_auth_key.strip()
        sqladmin_auth_key = make_none_if_blank(sqladmin_auth_key)

        if get_cached_settings().sqladmin_auth_keys is not None:
            if sqladmin_auth_key is not None and sqladmin_auth_key in get_cached_settings().sqladmin_auth_keys:
                return True

        return False

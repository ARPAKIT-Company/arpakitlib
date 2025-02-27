from fastapi import FastAPI
from sqladmin import Admin

from core.settings import get_cached_settings
from sqladmin_.admin_auth import SQLAdminAuth
from sqladmin_.model_view import get_simple_mv
from sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def add_sqladmin_in_app(*, app: FastAPI, base_url: str = "/sqladmin") -> FastAPI:
    authentication_backend = SQLAdminAuth()

    admin = Admin(
        app=app,
        engine=get_cached_sqlalchemy_db().engine,
        base_url=base_url,
        authentication_backend=authentication_backend,
        title=get_cached_settings().project_name
    )

    for model_view in get_simple_mv().__subclasses__():
        admin.add_model_view(model_view)

    return app

from fastapi import FastAPI
from sqladmin import Admin

from admin1.admin_auth import Admin1Auth
from admin1.model_view import get_simple_mv
from core.settings import get_cached_settings
from sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


def add_admin1_in_app(*, app: FastAPI) -> FastAPI:
    authentication_backend = Admin1Auth()

    admin = Admin(
        app=app,
        engine=get_cached_sqlalchemy_db().engine,
        base_url="/admin1",
        authentication_backend=authentication_backend,
        title=get_cached_settings().project_name
    )

    for model_view in get_simple_mv().__subclasses__():
        admin.add_model_view(model_view)

    return app

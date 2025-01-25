import importlib
from contextlib import suppress

from fastapi import FastAPI
from sqladmin import Admin

from arpakitlib.ar_sqladmin_util import SimpleModelView
from src.admin1.admin_auth import AdminAuth
from src.api.transmitted_api_data import TransmittedAPIData
from src.core.settings import get_cached_settings


def add_admin1_in_app(*, app: FastAPI) -> FastAPI:
    transmitted_api_data: TransmittedAPIData = app.state.transmitted_api_data

    authentication_backend = AdminAuth()

    admin = Admin(
        app=app,
        engine=transmitted_api_data.sqlalchemy_db.engine,
        base_url="/admin1",
        authentication_backend=authentication_backend,
        title=get_cached_settings().project_name
    )

    with suppress(Exception):
        importlib.import_module("src.admin1.model_view")

    for model_view in SimpleModelView.all_subclasses:
        admin.add_model_view(model_view)

    return app

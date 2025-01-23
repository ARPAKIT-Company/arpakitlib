from fastapi import FastAPI
from sqladmin import Admin

from src.admin1.admin_auth import AdminAuth
from src.admin1.model_view import MODEL_VIEWS
from src.api.transmitted_api_data import TransmittedAPIData


def add_admin1_in_app(*, app: FastAPI) -> FastAPI:
    transmitted_api_data: TransmittedAPIData = app.state.transmitted_api_data

    authentication_backend = AdminAuth()

    admin = Admin(
        app=app,
        engine=transmitted_api_data.sqlalchemy_db.engine,
        base_url="/admin1",
        authentication_backend=authentication_backend,
        title="{PROJECT_NAME}"
    )

    for model_view in MODEL_VIEWS:
        admin.add_model_view(model_view)

    return app

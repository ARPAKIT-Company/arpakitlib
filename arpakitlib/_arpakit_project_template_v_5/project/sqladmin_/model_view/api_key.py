import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


class ApiKeyMV(SimpleMV, model=ApiKeyDBM):
    name = "ApiKey"
    name_plural = "ApiKeys"
    icon = "fa-solid fa-key"
    column_list = sqlalchemy.inspect(ApiKeyDBM).columns
    form_columns = [
        ApiKeyDBM.slug,
        ApiKeyDBM.title,
        ApiKeyDBM.value,
        ApiKeyDBM.is_active,
    ]
    column_sortable_list = sqlalchemy.inspect(ApiKeyDBM).columns
    column_default_sort = [
        (ApiKeyDBM.creation_dt, True)
    ]
    column_searchable_list = [
        ApiKeyDBM.id,
        ApiKeyDBM.long_id,
        ApiKeyDBM.slug,
        ApiKeyDBM.value,
    ]
    column_formatters = {
        ApiKeyDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }
    column_formatters_detail = {
        ApiKeyDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }

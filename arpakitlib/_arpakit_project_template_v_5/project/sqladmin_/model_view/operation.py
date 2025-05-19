import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class OperationMV(SimpleMV, model=OperationDBM):
    name = "Operation"
    name_plural = "Operations"
    icon = "fa-solid fa-gears"
    column_list = sqlalchemy.inspect(OperationDBM).columns
    form_columns = [
        OperationDBM.slug,
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.title,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data,
        OperationDBM.extra_data
    ]
    column_sortable_list = sqlalchemy.inspect(OperationDBM).columns
    column_default_sort = [
        (OperationDBM.creation_dt, True)
    ]
    column_searchable_list = [
        OperationDBM.id,
        OperationDBM.long_id,
        OperationDBM.slug,
    ]
    column_formatters = {
        OperationDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }
    column_formatters_detail = {
        OperationDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }

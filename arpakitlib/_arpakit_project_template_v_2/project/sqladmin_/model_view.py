from sqladmin import ModelView

from arpakitlib.ar_sqladmin_util import get_string_info_from_model_view
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM, OperationDBM


class SimpleMV(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    page_size = 50
    page_size_options = [50, 100, 200]
    save_as = True
    save_as_continue = True
    export_types = ["xlsx", "csv", "json"]


class StoryLogMV(SimpleMV, model=StoryLogDBM):
    name = "StoryLog"
    name_plural = "StoryLogs"
    column_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
        StoryLogDBM.creation_dt,
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.data
    ]
    form_columns = [
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.data
    ]
    column_default_sort = [
        (StoryLogDBM.creation_dt, True)
    ]
    column_searchable_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.data
    ]


class OperationMV(SimpleMV, model=OperationDBM):
    name = "Operation"
    name_plural = "Operations"
    column_list = [
        OperationDBM.id,
        OperationDBM.long_id,
        OperationDBM.creation_dt,
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data
    ]
    form_columns = [
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data
    ]
    column_default_sort = [
        (OperationDBM.creation_dt, True)
    ]
    column_searchable_list = [
        OperationDBM.id,
        OperationDBM.long_id,
        OperationDBM.status,
        OperationDBM.type,
    ]


def get_simple_mv() -> type[SimpleMV]:
    return SimpleMV


def import_sqladmin_model_views():
    pass


if __name__ == '__main__':
    print(get_string_info_from_model_view(class_=SimpleMV))

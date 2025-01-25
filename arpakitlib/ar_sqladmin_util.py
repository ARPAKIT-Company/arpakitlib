# arpakit
from sqladmin import ModelView
from sqladmin.models import ModelViewMeta

from arpakitlib.ar_class_util import CollectingSubclassesMeta
from arpakitlib.ar_sqlalchemy_model_util import OperationDBM, StoryLogDBM

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def create_combined_meta(*metas):
    """
    Создает объединённый метакласс для устранения конфликтов.
    """

    class CombinedMeta(*metas):
        pass

    return CombinedMeta


class SimpleModelView(ModelView, metaclass=create_combined_meta(CollectingSubclassesMeta, ModelViewMeta)):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    save_as = True
    save_as_continue = True
    export_types = ["xlsx", "csv", "json"]


class OperationMV(SimpleModelView, model=OperationDBM):
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


class StoryLogMV(SimpleModelView, model=StoryLogDBM):
    name = "StoryLog"
    name_plural = "StoryLogs"
    column_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
        StoryLogDBM.creation_dt,
        StoryLogDBM.level,
        StoryLogDBM.title,
        StoryLogDBM.data
    ]
    form_columns = [
        StoryLogDBM.level,
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
        StoryLogDBM.title,
        StoryLogDBM.data
    ]


def __example():
    print(len(SimpleModelView.all_subclasses))
    for model_view in SimpleModelView.all_subclasses:
        print(model_view)


if __name__ == '__main__':
    __example()

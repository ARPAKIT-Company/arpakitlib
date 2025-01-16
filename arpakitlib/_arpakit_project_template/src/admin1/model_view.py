from sqladmin import ModelView


class BaseModelView(ModelView):
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

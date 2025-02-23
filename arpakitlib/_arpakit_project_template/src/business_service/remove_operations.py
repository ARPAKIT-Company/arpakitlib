from arpakitlib.ar_type_util import raise_for_type
from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM


def remove_operations(
        *,
        filter_operation_ids: list[int] | int | None = None,
        filter_operation_types: list[str] | str | None = None,
        filter_operation_statuses: list[str] | str | None = None
):
    if isinstance(filter_operation_ids, int):
        filter_operation_ids = [filter_operation_ids]
    if filter_operation_ids is not None:
        raise_for_type(filter_operation_ids, list)

    if isinstance(filter_operation_types, str):
        filter_operation_types = [filter_operation_types]
    if filter_operation_types is not None:
        raise_for_type(filter_operation_types, list)

    if isinstance(filter_operation_statuses, str):
        filter_operation_statuses = [filter_operation_statuses]
    if filter_operation_statuses is not None:
        raise_for_type(filter_operation_statuses, list)

    with get_cached_sqlalchemy_db().new_session() as session:
        query = session.query(OperationDBM)
        if filter_operation_ids is not None:
            query = query.filter(OperationDBM.id.in_(filter_operation_ids))
        if filter_operation_types is not None:
            query = query.filter(OperationDBM.type.in_(filter_operation_types))
        if filter_operation_statuses is not None:
            query = query.filter(OperationDBM.status.in_(filter_operation_statuses))
        query.delete()
        session.commit()

from sqlalchemy.exc import NoResultFound

from src.sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM


def get_operation(
        *,
        filter_operation_id: int,
        raise_if_not_found: bool = False,
) -> OperationDBM | None:
    with get_cached_sqlalchemy_db().new_session() as session:
        query = (
            session
            .query(OperationDBM)
            .filter(OperationDBM.id == filter_operation_id)
        )

        if raise_if_not_found:
            try:
                return query.one()
            except NoResultFound:
                if raise_if_not_found:
                    raise ValueError("operation not found")
        else:
            return query.one_or_none()


def __example():
    print(get_operation(filter_operation_id=214))


if __name__ == '__main__':
    __example()

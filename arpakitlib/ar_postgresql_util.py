# arpakit

from arpakitlib.ar_run_cmd_util import run_cmd
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def make_postgresql_db_dump(
        *,
        user: str,
        host: str = "127.0.0.1",
        db_name: str,
        port: int = 5432,
        out_filepath: str = "db_dump.sql",
        password: str | None = None
) -> str:
    raise_for_type(user, str)
    raise_for_type(host, str)
    raise_for_type(db_name, str)
    raise_for_type(port, int)
    if password:
        run_cmd_res = run_cmd(
            command=f"echo {password} | pg_dump -U {user} -h {host} {db_name} -p {port} > {out_filepath}"
        )
    else:
        run_cmd_res = run_cmd(
            command=f"pg_dump -U {user} -h {host} {db_name} -p {port} > {out_filepath}"
        )
    run_cmd_res.raise_for_bad_return_code()

    return out_filepath


def __example():
    user = "test_user"
    host = "localhost"
    db_name = "test_db"
    port = 5432
    out_filepath = "test_dump.sql"
    password = "test_password"

    result_path = make_postgresql_db_dump(
        user=user,
        host=host,
        db_name=db_name,
        port=port,
        out_filepath=out_filepath,
        password=password
    )
    print(f"Дамп базы данных сохранен в файл {result_path}")


if __name__ == '__main__':
    __example()

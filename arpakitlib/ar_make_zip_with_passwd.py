# arpakit

import pyminizip


def make_zip_with_passwd(
        *,
        input_filepath: str
):
    pyminizip.compress(
        input_filepath,  # исходный файл
        None,
        "dump.sql.zip",  # архив
        "super_secret",  # пароль
        5  # уровень сжатия (1–9)
    )

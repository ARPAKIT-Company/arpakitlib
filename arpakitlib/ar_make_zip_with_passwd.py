# arpakit

import pyminizip


def make_zip_with_passwd(
        *,
        input_filepath: str,
        output_filename: str = "archive.zip",
        passwd: str = "123"
):
    pyminizip.compress(
        input_filepath,  # исходный файл
        "./asf/asf",
        output_filename,  # архив
        passwd,  # пароль
        5  # уровень сжатия (1–9)
    )


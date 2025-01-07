# arpakit

from typing import Any

import pandas

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def list_of_dicts_to_xlsx(
        list_of_dicts: list[dict[str, Any]],
        out_filepath: str = "out.xlsx",
        sheet_name: str = "Sheet 1"
) -> str:
    data_frame = pandas.DataFrame(list_of_dicts)

    writer = pandas.ExcelWriter(out_filepath, engine="xlsxwriter")
    data_frame.to_excel(writer, index=False, sheet_name=sheet_name)

    for i, col in enumerate(data_frame.columns):
        width = max(data_frame[col].apply(lambda x: len(str(x))).max(), len(col))
        writer.sheets[sheet_name].set_column(i, i, width * 1.1)

    writer._save()

    return out_filepath


def __example():

    data = [
        {"Name": "Name1", "Age": 22, "City": "Ufa"},
        {"Name": "Name2", "Age": 20, "City": "Moscow"},
        {"Name": "Name3", "Age": 35, "City": "Baymak"}
    ]

    list_of_dicts_to_xlsx(list_of_dicts=data, out_filepath="output_file.xlsx", sheet_name="Test")


if __name__ == '__main__':
    __example()

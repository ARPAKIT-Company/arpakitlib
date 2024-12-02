import json

from arpakitlib.ar_arpakit_lib_module_util import get_arpakit_lib_modules

_ARPAKIT_LIB_MODULE_VERSION = "1.5"

if __name__ == '__main__':
    arpakit_lib_modules = get_arpakit_lib_modules()

    print("module_name_to_module_version big json")
    print(json.dumps(arpakit_lib_modules.module_name_to_module_version(), ensure_ascii=False, indent=2))
    print()

    print("module_names_who_has_error big json")
    print(json.dumps(arpakit_lib_modules.module_names_who_has_errors(), ensure_ascii=False, indent=2))
    print()

    print("module_name_to_module_exception big json")
    print(json.dumps(arpakit_lib_modules.module_name_to_module_exception(
        filter_module_has_error=True
    ), ensure_ascii=False, indent=2, default=str))
    print()

    print("modules_hash")
    print(json.dumps(arpakit_lib_modules.modules_hash(), ensure_ascii=False))
    print()

    print("module_name_to_module_hash in small json")
    print(json.dumps(arpakit_lib_modules.module_name_to_module_hash(), ensure_ascii=False))
    print()

    print("module_name_to_module_version small json")
    print(json.dumps(arpakit_lib_modules.module_name_to_module_version(), ensure_ascii=False))
    print()

    print(arpakit_lib_modules)

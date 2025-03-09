from arpakitlib.ar_enumeration_util import Enumeration


class GeneralCommandsTgBot(Enumeration):
    healthcheck = "healthcheck"
    hello_world = "hello_world"


class ClientCommandsTgBot(Enumeration):
    start = "start"
    about = "about"


class AdminCommandsTgBot(Enumeration):
    arpakitlib_project_template_info = "arpakitlib_project_template_info"
    admin_healthcheck = "admin_healthcheck"
    init_db = "init_db"
    reinit_db = "reinit_db"
    drop_db = "drop_db"
    set_tg_bot_commands = "set_tg_bot_commands"
    raise_fake_err = "raise_fake_err"
    log_file = "log_file"
    clear_log_file = "clear_log_file"
    kb_with_old_data = "kb_with_old_data"
    kb_with_not_modified = "kb_with_not_modified"
    kb_with_fake_error = "kb_with_fake_error"
    kb_with_remove_message = "kb_with_remove_message"


def __example():
    print("GeneralCommandsTgBot:")
    for v in GeneralCommandsTgBot.values_list():
        print(f"- {v}")
    print()
    print("ClientCommandsTgBot:")
    for v in ClientCommandsTgBot.values_list():
        print(f"- {v}")
    print()
    print("AdminCommandsTgBot:")
    for v in AdminCommandsTgBot.values_list():
        print(f"- {v}")


if __name__ == '__main__':
    __example()

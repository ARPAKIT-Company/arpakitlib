from arpakitlib.ar_enumeration_util import Enumeration


class ClientTgBotCommands(Enumeration):
    start = "start"
    about = "about"
    healthcheck = "healthcheck"
    hello_world = "hello_world"


class AdminTgBotCommands(Enumeration):
    arpakitlib_project_template_info = "arpakitlib_project_template_info"
    init_db = "init_db"
    reinit_sqlalchemy_db = "reinit_sqlalchemy_db"
    drop_db = "drop_db"
    set_tg_bot_commands = "set_tg_bot_commands"
    raise_fake_err = "raise_fake_err"
    me = "me"
    log_file = "log_file"
    clear_log_file = "clear_log_file"
    kb_with_old_data = "kb_with_old_data"
    kb_with_not_modified = "kb_with_not_modified"
    kb_with_fake_error = "kb_with_fake_error"
    kb_with_remove_message = "kb_with_remove_message"


def __example():
    print("ClientCommandsTgBot:")
    for v in ClientTgBotCommands.values_list():
        print(f"- {v}")
    print()
    print("AdminCommandsTgBot:")
    for v in AdminTgBotCommands.values_list():
        print(f"- {v}")


if __name__ == '__main__':
    __example()

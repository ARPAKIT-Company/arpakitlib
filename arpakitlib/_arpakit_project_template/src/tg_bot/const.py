from arpakitlib.ar_enumeration_util import Enumeration


class TgBotPublicCommands(Enumeration):
    start = "start"


class TgBotPrivateCommands(Enumeration):
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

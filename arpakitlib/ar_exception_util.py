import traceback


def exception_to_traceback_str(exception: BaseException) -> str:
    return "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

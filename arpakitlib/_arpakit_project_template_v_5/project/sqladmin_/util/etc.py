import datetime as dt
import json
from typing import Any

from arpakitlib.ar_json_util import transfer_data_to_json_str
from markupsafe import Markup
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from pygments.style import Style
from pygments.token import Text


def format_datetime_(datetime_: dt.datetime | None) -> str:
    if datetime_ is None:
        return ""
    return datetime_.strftime("%Y-%m-%d %H:%M:%S")


def format_json_for_preview_(data: dict[str, Any] | list[Any] | None) -> str:
    if data is None:
        return ""
    return f"JSON {type(data)} ({len(data)} элементов)"


def format_json_(data: dict[str, Any] | list[Any] | None) -> str:
    if data is None:
        return Markup("")
    highlighted_json = highlight(
        transfer_data_to_json_str(data, beautify=True),
        JsonLexer(),
        HtmlFormatter()
    )
    return Markup(highlighted_json)


def format_link_(
        link: str | None = None,
) -> str:
    if link is None:
        return ""
    return Markup(f'<a href="{link}" target="_blank">{link}</a>')
